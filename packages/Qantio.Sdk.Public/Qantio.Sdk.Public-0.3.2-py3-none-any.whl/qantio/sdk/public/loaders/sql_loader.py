import uuid
import pyodbc
import pandas as pd
from qantio.sdk.public.connectors.pandas_loader import QantioAccessor
from qantio.sdk.public.models import TimeSerie

import logging
logger = logging.getLogger(__name__)

def load(
    id                  : uuid.UUID,
    driver              : str,
    server              : str,
    username            : str,
    password            : str,
    database            : str,
    query               : str,
    time_col            : str, 
    observations_cols   : list, 
    dimensions_cols     : list=[], 
    exogenous_cols      : list=[]
    )->TimeSerie:
    

    logger.info(f"{driver} > {server} > {database}")
    
    con_string = 'DRIVER={'+driver+'};SERVER='+ server +';DATABASE='+ database +';UID='+ username +';PWD='+ password
    cnxn = pyodbc.connect(con_string)
    cursor = cnxn.cursor()
  
    df = pd.read_sql(query, cnxn)
    df.attrs['metadata'] = {'origin':driver,"server":server, "database":database}

    return df.qantio.to_timeserie(
            id                  = id, 
            time_col            = time_col, 
            observations_cols   = observations_cols, 
            dimensions_cols     = dimensions_cols,
            exogenous_cols      = exogenous_cols,
            )