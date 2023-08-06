import uuid
import pandas as pd

from qantio.sdk.public.connectors import aws_s3, azure_blob, csv, ftp, sql
from qantio.sdk.public.models.timeserie import TimeSerie

class DataSource:
    """
        The base object to load data into qant.io time series format.
    """
    def sql(
        id                  : uuid.UUID, 
        driver              : str, 
        server              : str, 
        username            : str, 
        password            : str, 
        database            : str, 
        query               : str, 
        time_col            : str, 
        observations_cols   : list, 
        dimensions_cols     : list = [], 
        exogenous_cols      : list = []
        )->TimeSerie:
            """
                Create a qant.io time serie from SQL data.
            
            """
            return sql.load(**{key: value for key, value in locals().items() if key not in 'self'})
    
    
    def ftp(
        id                  : uuid.UUID,
        host                : str, 
        username            : str, 
        password            : str, 
        directory           : str, 
        file                : str, 
        time_col            : str, 
        observations_cols   : list, 
        dimensions_cols     : list = [], 
        exogenous_cols      : list = [], 
        index_col           : bool = False, 
        header              : int = 0, 
        sep                 : str = ";"
        )->TimeSerie:
            """
                Create a qant.io time serie from a file on a FTP server.
            
            """
            return ftp.load(**{key: value for key, value in locals().items() if key not in 'self'})
    
    
    def csv(
        id                  : uuid.UUID, 
        file_path           : str, 
        time_col            : str, 
        observations_cols   : list, 
        dimensions_cols     : list = [], 
        exogenous_cols      : list = [], 
        index_col           : bool = False, 
        header              : int = 0, 
        sep                 : str = ";"
        )->TimeSerie:
            """
                Create a qant.io time serie from a file local CSV file.
            
            """
            return csv.load(**{key: value for key, value in locals().items() if key not in 'self'})
    
    def pandas_dataframe(
        df                  : pd.DataFrame,
        id                  : uuid,
        time_col            : str, 
        observations_cols   : list, 
        dimensions_cols     : list=[], 
        exogenous_cols      : list=[],)->TimeSerie:
        """
            Create a qant.io time serie from a pandas dataframe.
            
        """
        df.attrs['metadata'] = {'origin':'user dataframe'}
        return df.qantio.to_timeserie(**{key: value for key, value in locals().items() if key not in 'df'})

    def aws_s3(
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
        """
            Create a qant.io time serie from a file in a Amazon S3 bucket.
            
        """
        return aws_s3.load(**{key: value for key, value in locals().items() if key not in 'self'})
    
    def azure_blob(
        id                  : uuid, 
        account             : str, 
        account_key         : str, 
        container           : str, 
        file                : str, 
        time_col            : str, 
        observations_cols   : list, 
        dimensions_cols     : list = [], 
        exogenous_cols      : list = [], 
        index_col           : bool = False, 
        header              : int = 0, 
        sep                 : str = ";"
    )->TimeSerie:
        """
            Create a qant.io time serie from an Azure blob file.
            
            Args:
                id (uuid)                           : the time serie unique identifier
                account (str)                       : azure account
                account_key (str)                   : azure account key
                container (str)                     : azure container
                file (str)                          : _description_
                time_col (str)                      : _description_
                observations_cols (list)            : _description_
                dimensions_cols (list, optional)    : _description_. Defaults to [].
                exogenous_cols (list, optional)     : _description_. Defaults to [].
                index_col (bool, optional)          : _description_. Defaults to False.
                header (int, optional)              : _description_. Defaults to 0.
                sep (str, optional)                 : _description_. Defaults to ";".

            Returns:
                TimeSerie: _description_
        """
        return azure_blob.load(**{key: value for key, value in locals().items() if key not in 'self'})