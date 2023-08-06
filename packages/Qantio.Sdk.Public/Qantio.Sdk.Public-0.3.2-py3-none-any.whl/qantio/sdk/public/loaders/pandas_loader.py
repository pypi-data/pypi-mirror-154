
import uuid
import pandas as pd
from qantio.sdk.public.models import TimeSerie, DataPoint

import logging
logger = logging.getLogger("qantio.sdk.importers.timeserie")

@pd.api.extensions.register_dataframe_accessor("qantio")
class QantioAccessor:
    df:pd.DataFrame
    
    def __init__(self, dataframe:pd.DataFrame):
        self.df = dataframe
        
    def to_timeserie(
        self, 
        id                  : uuid, 
        time_col            : str, 
        observations_cols   : set, 
        dimensions_cols     : set=[], 
        exogenous_cols      : set=[],)->TimeSerie:
        
        # Guards
        if self.df is None:
            err = f"The pandas dataframe is missing."
            logger.error(err)
            exit()
        
        if len(self.df)==0:
            logger.error(f"The pandas dataframe contains no data.")
            exit()

        if not observations_cols:
            logger.error(f"observations_cols is empty. At least one observation column is requiered.")
            exit()

        df_columns = self.df.columns

        # Check time_col
        if not time_col in df_columns:
            err = f"time column <{time_col}> not found in pandas dataframe"
            logger.error(err)
            exit()

        # Check observations_cols
        missing_observations = list(set(observations_cols).difference(df_columns))
        if missing_observations:
            err = f"observation column(s) <{missing_observations}> not found in pandas dataframe"
            logger.error(err)
            exit()

        # Check dimensions_cols
        missing_dimensions = set(dimensions_cols).difference(df_columns)
        if missing_dimensions:
            err = f"dimension column(s) <{missing_dimensions}> not found in pandas dataframe"
            logger.warning(err)
            logger.warning(f'<{missing_dimensions}> was/where removed from exogenous column(s)')
            dimensions_cols = set(dimensions_cols).difference(missing_dimensions)

        # Check exogenous_cols
        missing_exogenous = list(set(exogenous_cols).difference(df_columns))
        if missing_exogenous:
            err = f"exogenous column(s) <{missing_exogenous}> not found in pandas dataframe"
            logger.warning(err)
            logger.warning(f'<{missing_exogenous}> was/where removed from exogenous column(s)')
            exogenous_cols = set(exogenous_cols).difference(missing_exogenous)

        self.df[time_col] = pd.to_datetime(self.df[time_col])

        # Dataframe to records
        records = self.df.to_dict(orient='records')

        datapoints:list[DataPoint] = []
        
        for record in records:
            
            # Make DataPoint
            dtp = DataPoint(
                timestamp           = record[time_col], 
                observation_name    = None, 
                observation_value   = None, 
                observations        = dict([(obs,record[obs]) for obs in observations_cols]), 
                dimensions          = dict([(dim,record[dim]) for dim in dimensions_cols]),
                exogenous           = dict([(exo,record[exo]) for exo in exogenous_cols]),
                place               = None
            )
           
            datapoints.append(dtp)
        
        # Make TimeSerie
        ts = TimeSerie(id)
        ts.add_measurements(datapoints=datapoints)
        logger.log(11, f"Time serie <{ts.dataset_identifier}> with {len(ts.datapoints)} datapoint(s) was created from source {self.df.attrs['metadata']}.")
        
        # Return it
        return ts