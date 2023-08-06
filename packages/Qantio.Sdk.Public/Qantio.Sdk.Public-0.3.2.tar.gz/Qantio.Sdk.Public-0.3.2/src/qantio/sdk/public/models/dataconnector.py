from dataclasses import dataclass, field
import uuid
import boto3
import logging
import pandas as pd
from typing import TYPE_CHECKING

#============================================
from qantio.sdk.public.connectors import aws_s3
#============================================

if TYPE_CHECKING:
    from qantio.sdk.public.models.dataconnector import TimeSerieAdapterSettings
    from qantio.sdk.public.models.timeserie import TimeSerie

logger = logging.getLogger(__name__)

@dataclass
class Connector():
    settings:any

@dataclass
class TimeSerieAdapterSettings():
    id                  : uuid
    name                : str
    time_col            : str
    observations_cols   : list
    dimensions_cols     : list  = field(default_factory=list) 
    exogenous_cols      : list  = field(default_factory=list) 
    index_col           : bool  = False
    header              : int   = 0
    sep                 : str   = ";"


@dataclass
class AzureBlobConnectorSettings():
    account             : str
    account_key         : str
    container           : str
    file                : str


@dataclass
class AwsS3ConnectorSettings():
    bucket              : str
    file                : str
    access_key_id       : str
    secret_access_key   : str
    session_token       : str = None
    directory           : str = ""
    

@dataclass
class AzureBlobDataConnector(Connector):
    settings : AzureBlobConnectorSettings
    
    def load(self, timeserie_settings:'TimeSerieAdapterSettings')->'TimeSerie':
        pass
   
    def push(self)->'TimeSerie':
        pass

@dataclass
class AwsS3DataConnector(Connector):
    settings : AwsS3ConnectorSettings
    
    def load(self, timeserie_settings:'TimeSerieAdapterSettings')->'TimeSerie':
        return aws_s3.load(self.settings, timeserie_settings)
    
    def push(self)->'TimeSerie':
        pass