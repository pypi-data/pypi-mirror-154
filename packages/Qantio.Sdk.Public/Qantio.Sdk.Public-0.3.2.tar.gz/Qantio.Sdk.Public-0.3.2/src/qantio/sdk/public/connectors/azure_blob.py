import uuid
import pandas as pd
from io import BytesIO

from azure.storage.blob import BlobServiceClient

#============================================
from qantio.sdk.public.connectors.pandas_loader import QantioAccessor
from qantio.sdk.public.models.timeserie import TimeSerie
#============================================

import logging
logger = logging.getLogger(__name__)

def load(
    id                  : uuid.UUID,
    account             : str,
    account_key         : str,
    container           : str,
    file                : str,
    time_col            : str, 
    observations_cols   : list, 
    dimensions_cols     : list=[], 
    exogenous_cols      : list=[],
    index_col           : bool  = False, 
    header              : int   = 0, 
    sep                 : str   = ";"
    )->TimeSerie:
    
    logger.info(f"azure blob storage > {container} > {file}")
    
    account_conn_string = f"DefaultEndpointsProtocol=https;AccountName={account};AccountKey={account_key};EndpointSuffix=core.windows.net"
    blob_client = BlobServiceClient.from_connection_string(conn_str=account_conn_string).get_blob_client(container=container, blob=file)

    file_bytes = None
    try:
        file_bytes = blob_client.download_blob().readall()
    except Exception as err:
        logger.critical(err)
        raise(err)
    
    df = pd.read_csv(BytesIO(file_bytes), index_col=index_col, header=header, sep=sep)
    df.attrs['metadata'] = {'origin':"azure blob storage", "container":container, "file":file}
   
    return df.qantio.to_timeserie(
            id                  = id, 
            time_col            = time_col, 
            observations_cols   = observations_cols, 
            dimensions_cols     = dimensions_cols,
            exogenous_cols      = exogenous_cols,
            )