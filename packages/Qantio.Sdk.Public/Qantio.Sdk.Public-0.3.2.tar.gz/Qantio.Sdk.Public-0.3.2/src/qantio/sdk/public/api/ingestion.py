import asyncio
import json
import aiohttp
from aiohttp import ClientSession
import urllib3
from joblib import Parallel, delayed
from requests_toolbelt import sessions
from typing import TYPE_CHECKING

#============================================
from qantio.sdk.public.common.settings import qantio_settings
from qantio.sdk.public.models.batch_operation_result import BatchOperationResult
from qantio.sdk.public.models.operation_result import OperationResult
#============================================

if TYPE_CHECKING:
    from qantio.sdk.public.models.timeserie import TimeSerie

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SETTINGS = qantio_settings()['api']['services']['timeseries']

def __map_response(
    idx         : int,
    payload     : json,
    response    : json, 
    status_code : int, 
    headers     : dict)->BatchOperationResult:

    result = BatchOperationResult(
            Index           = idx,
            DataPoints      = int(len(payload)),
            Success         = response.get('success'),
            StatusCode      = status_code,
            ResponseHeaders = headers,
            ResponseErrors  = response.get('errors'),
            Duration        = response.get('duration'),
            BytesProcessed  = response.get('bytesProcessed')
        )

    return result.finalize()

async def __post_data_async(session:aiohttp.ClientSession, payload:json):
    
    async with session.post(url = SETTINGS['ingestion'], json = payload) as resp:
        response = await resp.json()
        return payload, response, resp.status, resp.headers

def __post_data_sync(idx:int, payload, http_client:sessions.BaseUrlSession, base_url, headers)->BatchOperationResult:
    
    if http_client.base_url is None:
        http_client.base_url = base_url

    response = http_client.post(
        url     = SETTINGS['ingestion'], 
        headers = headers, 
        json    = payload, 
        verify  = False
    )

    return __map_response(
        idx         = idx, 
        payload     = payload, 
        response    = response.json(), 
        status_code = response.status_code, 
        headers     = response.headers).finalize()

async def ingest_async(
    timeserie           : 'TimeSerie', 
    http_client         : sessions.BaseUrlSession, 
    batch_size          : int=500, 
    ingest_properties   : bool=True, 
    operation_name      : str = "Timeserie async ingestion")->BatchOperationResult:
    
    """
        Send time serie to qant.io ingestion service
    
    """
    print("ingest async")
    
    batches = timeserie.to_batches(batch_size) #[payload[x:x+batch_size] for x in range(0, len(payload), batch_size)]
    
    headers = http_client.headers
    base_url = http_client.base_url
    
    # Make OperationResult
    operation_result = OperationResult(OperationName = operation_name)
    
    async with ClientSession(headers = headers, base_url = base_url) as session:
        
        tasks = []
        for b in batches:
            tasks.append(asyncio.ensure_future(__post_data_async(session, b)))

        responses = await asyncio.gather(*tasks)
        
        for idx,response in enumerate(responses):
            operation_result.BatchOperations.append(__map_response(idx, response[0], response[1], response[2], dict(response[3])))

    return operation_result.finalize()
    

def ingest(
    timeserie:'TimeSerie', 
    http_client:sessions.BaseUrlSession, 
    batch_size:int=500, 
    n_jobs=1, 
    operation_name:str = "Timeserie sync ingestion")->OperationResult:
    
    """
        Send time serie to qant.io ingestion service
    """
    
    # Set batchs
    batchs = timeserie.to_batches(batch_size, http_client.headers.get('ClientId'))
   
    # Set OperationResult
    operation_result = OperationResult(OperationName = operation_name)

    #Run multiple jobs in //
    if n_jobs > 1:
        jobs = Parallel(n_jobs=n_jobs, backend='loky')(
            delayed(__post_data_sync)
                (idx, content, http_client, http_client.base_url, http_client.headers) for idx,content in enumerate(batchs)
            )

        operation_result.BatchOperations = jobs
        return operation_result.finalize()
    
    # Or run sequential jobs
    for idx, content in enumerate(batchs):
        operation_result.BatchOperations.append(__post_data_sync(
                idx         = idx, 
                payload     = content,
                http_client = http_client, 
                base_url    = http_client.base_url, 
                headers     = http_client.headers
            )
        )
       
    return operation_result.finalize()