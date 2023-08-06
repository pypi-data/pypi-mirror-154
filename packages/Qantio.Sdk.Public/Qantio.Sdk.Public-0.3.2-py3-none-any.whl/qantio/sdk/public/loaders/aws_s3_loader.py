import boto3
from io import BytesIO
import uuid
import pandas as pd
from pyparsing import original_text_for
from qantio.sdk.public.connectors.pandas_loader import QantioAccessor
from qantio.sdk.public.models import TimeSerie
import logging
logger = logging.getLogger(__name__)

def load(
    id                  : uuid.UUID,
    bucket              : str,
    access_key_id       : str,
    secret_access_key   : str,
    session_token       : str,
    directory           : str,
    file                : str,
    time_col            : str, 
    observations_cols   : list, 
    dimensions_cols     : list=[], 
    exogenous_cols      : list=[],
    index_col           : bool  = False, 
    header              : int   = 0, 
    sep                 : str   = ";"
    )->TimeSerie:
    
    logger.info(f"{bucket} > {file}")
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id       = access_key_id,
        aws_secret_access_key   = secret_access_key,
        aws_session_token       = session_token,
        )
    
    try:
        response = s3_client.get_object(Bucket=bucket, Key=f"{file}")
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
        index_col   = index_col, 
        header      = header, 
        sep         = sep)
    
    df.attrs['metadata'] = {'origin':"aws_s3", "bucket":bucket, "file":file}

    return df.qantio.to_timeserie(
            id                  = id, 
            time_col            = time_col, 
            observations_cols   = observations_cols, 
            dimensions_cols     = dimensions_cols,
            exogenous_cols      = exogenous_cols,
            )