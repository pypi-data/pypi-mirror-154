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

def save(id                  : uuid,
    file_path           : str,
    time_col            : str, 
    observations_cols   : list,  
    dimensions_cols     : list  = [], 
    exogenous_cols      : list  = [],
    index_col           : bool  = False, 
    header              : int   = 0, 
    sep                 : str   = ";")->OperationResult:
    pass

def load(
    id                  : uuid,
    file_path           : str,
    time_col            : str, 
    observations_cols   : list,  
    dimensions_cols     : list  = [], 
    exogenous_cols      : list  = [],
    index_col           : bool  = False, 
    header              : int   = 0, 
    sep                 : str   = ";")->TimeSerie:
    
    logger.info(f"{file_path}")

    settings = {'filepath_or_buffer':file_path, 'index_col':index_col, 'header':header, 'sep':sep}
    
    df = reader().read('csv', **settings)
    df.attrs['metadata'] = {'origin':"local csv", "file":file_path}
   
    return df.qantio.to_timeserie(
        id                  = id, 
        time_col            = time_col, 
        observations_cols   = observations_cols, 
        dimensions_cols     = dimensions_cols,
        exogenous_cols      = exogenous_cols,
    )