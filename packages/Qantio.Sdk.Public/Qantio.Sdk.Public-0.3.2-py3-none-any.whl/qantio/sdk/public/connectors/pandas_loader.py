
import uuid
import pandas as pd

from typing import TYPE_CHECKING

#============================================
from qantio.sdk.public.models.datapoint import DataPoint
from qantio.sdk.public.models.timeserie import TimeSerie
#============================================

if TYPE_CHECKING:
    from qantio.sdk.public.models.dataconnector import TimeSerieAdapterSettings
    
import logging
logger = logging.getLogger("qantio.sdk.public.importers.timeserie")

@pd.api.extensions.register_dataframe_accessor("qantio")
class QantioAccessor:
    df:pd.DataFrame
    
    def __init__(self, dataframe:pd.DataFrame):
        self.df = dataframe
        
    def to_timeserie(
        self, 
        timeserie_settings:'TimeSerieAdapterSettings')->TimeSerie:
        
        time_col            = timeserie_settings.time_col
        observations_cols   = timeserie_settings.observations_cols
        dimensions_cols     = timeserie_settings.dimensions_cols
        exogenous_cols      = timeserie_settings.exogenous_cols

        # Guards
        if self.df is None:
            err = f"The pandas dataframe is missing."
            logger.error(err)
            raise Exception(err)
        
        if len(self.df)==0:
            err = f"The pandas dataframe contains no data."
            logger.error(f"")
            raise Exception(err)

        if not observations_cols:
            logger.error(f"observations_cols is empty. At least one observation column is requiered.")
            exit()

        df_columns = self.df.columns

        # Check time_col
        if not time_col in df_columns:
            err = f"time column <{timeserie_settings.time_col}> not found in pandas dataframe"
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
        time_serie = TimeSerie(timeserie_settings.id, timeserie_settings.name).add_measurements(datapoints)
        logger.log(11, f"Time serie <{time_serie.dataset_identifier}> with {len(time_serie.datapoints)} datapoint(s) was created from source {self.df.attrs['metadata']}.")
        
        # Return it
        return time_serie