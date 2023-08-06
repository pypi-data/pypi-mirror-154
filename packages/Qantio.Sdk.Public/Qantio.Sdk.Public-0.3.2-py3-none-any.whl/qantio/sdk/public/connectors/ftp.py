import ftplib
from io import BytesIO
import os
import uuid
import pandas as pd

#============================================
from qantio.sdk.public.connectors.pandas_loader import QantioAccessor
from qantio.sdk.public.models.timeserie import TimeSerie
from qantio.sdk.public.models.operation_result import OperationResult
from qantio.sdk.public.helpers.pandas_readers import reader
#============================================

import logging
logger = logging.getLogger(__name__)

def load(
    id                  : uuid.UUID,
    host                : str,
    username            : str,
    password            : str,
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
    
    logger.info(f"Loader > ftp > {host} > {directory} > {file}")
    
    bytes = BytesIO()
    ftp = ftplib.FTP(host=host,user=username,passwd=password)
    ftp.cwd(directory)
    ftp.retrbinary('RETR '+ file, bytes.write)
    bytes.seek(0)

    settings = {'filepath_or_buffer':bytes, 'index_col':index_col, 'header':header, 'sep':sep}
    file_extension = os.path.splitext(file)[1][1:]

    df = reader().read(file_extension, **settings)
    df.attrs['metadata'] = {'origin':"ftp", "directory":directory, "file":file}

    return df.qantio.to_timeserie(
        id                  = id, 
        time_col            = time_col, 
        observations_cols   = observations_cols, 
        dimensions_cols     = dimensions_cols,
        exogenous_cols      = exogenous_cols,
        )