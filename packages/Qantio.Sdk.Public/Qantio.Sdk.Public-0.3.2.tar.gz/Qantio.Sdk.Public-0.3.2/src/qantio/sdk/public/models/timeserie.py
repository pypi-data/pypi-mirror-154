from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import itertools
import warnings
import logging
import sys
import uuid
from typing import Callable, Dict, List, overload
from slugify import slugify
from datetime import datetime
import pandas as pd
from pandas_profiling import ProfileReport

#============================================
import qantio.sdk.public.models.experiment as exp
from qantio.sdk.public.api.ingestion import ingest as ingester, ingest_async as ingester_async
from qantio.sdk.public.client.qantio_client import QantioClient
from qantio.sdk.public.models.operation_result import OperationResult
from qantio.sdk.public.models.datapoint import DataPoint 
from qantio.sdk.public.models.geography_point import GeographyPoint 
#============================================

# warnings.simplefilter(action='ignore', category=FutureWarning)
logger = logging.getLogger(__name__)

class TimeSerie():
    """
        Main object to represent a time serie
        DataPoints : entities representing the time related data of the time serie
    """
    id                  : uuid.UUID
    name                : str               = ""
    slug                : str               = ""
    dataset_identifier  : str               = ""
    datapoints          : list[DataPoint]   = list()
    place               : GeographyPoint    = None         

    def __init__(self, id:uuid.UUID, name:str=""):
        self.Id = id
        self.name = name
        self.slug = slugify(name)
        self.dataset_identifier = f"qt_ts{str(id).replace('-', '').upper()}"

    def rename(self, name:str)->TimeSerie:
        """
            Name or rename the time serie
                
                Params :
                    
                    name : the name of the time serie
                
                Returns : the time serie renamed
        """
        self.name = name
        self.slug = slugify(name, separator=".")
        return self

    def preview(self, rows:int):
        return f"\n{self.to_dataframe().head(rows)}" 
    
    def remove_dimension(self, dimension:str)->TimeSerie:
        new_data_points = [d.dimensions for d in self.datapoints]
        return self

    def remove_observation(self, dimension:str)->TimeSerie:
        return self

    def remove_exogenous(self, dimension:str)->TimeSerie:
        return self

    def resample(self, rule:str='M')->TimeSerie:
        """
            Resample the time serie accordind to the pandas frequanbcy rule
            rule : 
                W         weekly frequency
                M         month end frequency
                SM        semi-month end frequency (15th and end of month)
        """
        #return TimeSerieManager().resample(self, rule)
        
        logger.info(f"Resampling time serie <{self.dataset_identifier}> by {rule}")

        obsersations_cols       = list(self._properties_names([d.observations for d in self.datapoints]))
        
        rename_strategy         = {x:f"{x.replace('obs_', '')}_{rule.lower()}" for x in obsersations_cols}
        new_observations_cols   = [f"{x.replace('obs_', '')}_{rule.lower()}"for x in obsersations_cols]

        df = self.to_dataframe().drop('time_ts', axis=1)
        df.time = pd.to_datetime(df.time)
        
        resample_df = df.resample(rule, on='time').sum().reset_index(inplace=False).rename(columns=dict(rename_strategy))
        
        resample_df.attrs['metadata'] = {"origin":"resampled"}

        self = resample_df.qantio.to_timeserie(
            id                  = self.Id, 
            time_col            = 'time', 
            observations_cols   = new_observations_cols, 
            dimensions_cols     = [],
            exogenous_cols      = [],)
        
        return self

    def group(self, by:list, agg:str, agg_funcs:list=['sum'])->TimeSerie:
        df = self.to_dataframe()
        grouped_df = df.groupby(by=by).agg({agg:agg_funcs})
        print(grouped_df.head())

    def _all_properties_names(self, validate=False):
        ts_properties = {
            'observations'  : list(self._properties_names([d.observations for d in self.datapoints])), 
            'dimensions'    : list(self._properties_names([d.dimensions for d in self.datapoints])), 
            'exogenous'     : list(self._properties_names([d.exogenous for d in self.datapoints])), 
            }
        if validate:
            validation_result = self.validate()
            ts_properties['isvalid']            = validation_result.Success
            ts_properties['errors']             = validation_result.Errors
            ts_properties['datapoints']         = validation_result.Outbound
            ts_properties['bytes']              = validation_result.Bytes
            ts_properties['validation_summary'] = validation_result.Summary
        
        return ts_properties

    def _properties_names(self, collection:dict)->list[str]:
        if len(self.datapoints)==0:
            return []
        return list(set(itertools.chain(*[list(o) for o in collection])))

    def add_measurement(self, datapoint:DataPoint) -> TimeSerie:
        self.datapoints.append(datapoint)
        return self

    # def measurement(self, timestamp:datetime, observation:float, dimension_name:str=None, dimension_value:str=None, place:GeographyPoint=None) -> TimeSerie:
    #     self.measurement(DataPoint(timestamp, dimension_name, dimension_value, observation, place))
    #     return self

    def add_measurements(self, datapoints:List[DataPoint])->TimeSerie:
        self.datapoints = datapoints
        return self
    
    def set_place(self, latitude:float, longitude:float, elevation:float=0)->TimeSerie:
        self.Place = GeographyPoint(latitude, longitude, elevation)
        return self
    
    def set_point(self, place:GeographyPoint)->TimeSerie:
        self.set_place(place)
        return self

    def filter(self, FilterFunc:Callable[[DataPoint], bool])->TimeSerie:
        logger.warning(f"Filtering time serie <{self.dataset_identifier}> with {FilterFunc.__name__}")
        self.datapoints = list(filter(FilterFunc, self.datapoints))
        return self

    def to_dataframe(self)->pd.DataFrame:
        return pd.DataFrame().from_records(data=[x['Record'] for x in self.to_payload('none')])
        
    def analyze(self):
        pass
        df = self.to_dataframe()
        analysys = df.describe()
        logger.log(11, df.info(verbose=True))
      
    def info(self, validate=False)->str:
        return {
            'id'                    : str(self.Id),
            'name'                  : str(self.name),
            'slug'                  : str(self.slug),
            'dataset_identifier'    : self.dataset_identifier,
            'datapoints'            : len(self.datapoints),
            'summary'               : self._all_properties_names(validate)
            }

    def to_batches(self, batch_size:int, client_id:str)->list():
        payload = self.to_payload(client_id)
        return [payload[x:x+batch_size] for x in range(0, len(payload), batch_size)]

    def validate(self)->OperationResult:
        
        """
            Validate the time serie according to ingestion rules

            returns : OperationResult
        """

        validation_result = OperationResult(OperationName="Time serie validation")

        if self is None:
            validation_result.Errors.append("TimeSerie is null")
            return validation_result.finalize()

        if not any(self.datapoints):
            validation_result.Errors.append("The time serie is empty, no data points where found. Rule : > 1")
            return validation_result.finalize()

        datapoints_counter = len(self.datapoints)
        if datapoints_counter>100000:
            validation_result.Errors.append("The time serie is too large to be ingested over http, please conctact us at suppor@qant.io. Rule : < 100 000")
            return validation_result.finalize()

        # Check that all data points have the same observations, dimensions and exogs
        ts_properties = self._all_properties_names()
        collections = ['observations', 'dimensions', 'exogenous']
        invalid_properties = []
        for collection in collections:
            for o in ts_properties[collection.lower()]:
                missing_obs_counter = len([x for x in self.datapoints if not(getattr(x, collection).get(o))])
                if missing_obs_counter>0:
                    invalid_properties.append({'type':collection.lower(), 'name':o, 'count':missing_obs_counter})
        
        if len(invalid_properties)>0:
            validation_result.Errors.append(f"{len(invalid_properties)} inconsistencies where found in time series data.")
            for invalid_property in invalid_properties:
                validation_result.Errors.append(f"In {invalid_property['type']} : <{invalid_property['name']}> is missing in {invalid_property['count']} measurement(s).")
            return validation_result.finalize()

        if len(ts_properties['observations']) == 0:
            validation_result.Errors.append("The time serie data points have no observations. Rule : > 1")
            return validation_result.finalize()

        if len(ts_properties['observations']) > 50:
            validation_result.Errors.append("Some data points contains too many observations. Rule : <= 50")
            return validation_result.finalize()

        if len(ts_properties['dimensions']) > 15:
            validation_result.Errors.append("Some data points contains too many dimensions. Rule : <= 15")
            return validation_result.finalize()

        if len(ts_properties['exogenous']) > 50:
            validation_result.Errors.append("Some data points contains too many exogenous values. Rule : <= 50")
            return validation_result.finalize()

        if len(set([x.timestamp for x in self.datapoints]))!=len(self.datapoints):
            validation_result.Errors.append("Some data points have the same time stamp. Each Data point must have a unique time stamp.")
            return validation_result.finalize()

        validation_result.Outbound  = len(self.datapoints)
        validation_result.Bytes     = sys.getsizeof(self)
        validation_result.Summary   = f"Time serie {self.dataset_identifier} is valid."
        
        return validation_result.finalize()

    def to_payload(self, client_id:str)->list():
        
        payload=[]
        
        for dtp in self.datapoints:
            
            entity = {
                "time"      : dtp.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "time_ts"   : float(datetime.timestamp(dtp.timestamp))
                }    
            
            for m in dtp.observations:
                entity[m]= float(dtp.observations[m])

            for d in dtp.dimensions:
                entity[d]= str(dtp.dimensions[d])

            for e in dtp.exogenous:
                entity[e]= float(dtp.exogenous[e])

            if dtp.place is not None:
                entity['prop_geo_latitude']     = dtp.place.latitude
                entity['prop_geo_longitude']    = dtp.place.longitude
                entity['prop_geo_elevation']    = dtp.place.elevation

            if not self.place is None:
                entity['prop_geo_latitude']     = self.place.latitude
                entity['prop_geo_longitude']    = self.place.longitude
                entity['prop_geo_elevation']    = self.place.elevation

            event_body = {  
                "TableContext"  : self.dataset_identifier,
                "Name"          : self.name,
                "Slug"          : self.slug,
                "ClientId"      : client_id,
                "Record"        : entity
                }
      
            payload.append(event_body)

        return payload

    def ingest(self, client:QantioClient, n_jobs:int)->OperationResult:
        return ingester(
            timeserie   = self, 
            http_client = client.http_client,
            batch_size  = 500, 
            n_jobs      = n_jobs
        )

    async def ingest_async(self, client:QantioClient, n_jobs:int)->OperationResult:
        return await ingester_async(
            timeserie   = self, 
            http_client = client.http_client,
            batch_size  = 500, 
            n_jobs      = n_jobs
        )

    def experiment(self, settings:exp.ExperimentSettings)->exp.Experiment:
        return exp.Experiment(
            settings    = settings, 
            time_serie  = self)