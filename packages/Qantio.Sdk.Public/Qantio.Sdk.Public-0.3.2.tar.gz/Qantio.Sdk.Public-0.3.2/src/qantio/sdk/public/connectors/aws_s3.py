import boto3
from io import BytesIO
import uuid
import pandas as pd
import logging
from typing import TYPE_CHECKING

#============================================
from qantio.sdk.public.connectors.pandas_loader import QantioAccessor
#============================================

if TYPE_CHECKING:
    from qantio.sdk.public.models.dataconnector import AwsS3ConnectorSettings, TimeSerieAdapterSettings
    from qantio.sdk.public.models.timeserie import TimeSerie

logger = logging.getLogger(__name__)

def load(
    settings            : 'AwsS3ConnectorSettings',
    timeserie_settings  : 'TimeSerieAdapterSettings'
    )-> 'TimeSerie':
    
    logger.info(f"{settings.bucket} > {settings.file}")
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id       = settings.access_key_id,
        aws_secret_access_key   = settings.secret_access_key,
        aws_session_token       = settings.session_token,
    )
    
    try:
        
        response = s3_client.get_object(
            Bucket=settings.bucket, 
            Key=settings.file
            )
        
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
   
    except Exception as e:
        logger.critical(e)
        raise Exception(e)

    # if not status==200:
    #     err = f"Loader > aws s3 > {file} > not found in bucket <{bucket}>"
    #     logger.error()
    #     raise Exception(err)
        
    df = pd.read_csv(
        response.get("Body"), 
        index_col   = timeserie_settings.index_col, 
        header      = timeserie_settings.header, 
        sep         = timeserie_settings.sep)
        
    df.attrs['metadata'] = {
        'origin'    : "aws_s3", 
        "bucket"    : settings.bucket, 
        "file"      : settings.file
        }

    return df.qantio.to_timeserie(timeserie_settings)