from __future__ import annotations
from dataclasses import dataclass, field
import json
from typing import TYPE_CHECKING
from dataclasses_json import dataclass_json
from enum import Enum
import asyncio
from time import sleep
import uuid

#============================================
import qantio.sdk.public.api.experiment_manager as experiment_manager
from qantio.sdk.public.client.qantio_client import QantioClient

from qantio.sdk.public.models.operation_result import OperationResult
if TYPE_CHECKING:
    from  qantio.sdk.public.models.timeserie import TimeSerie
    from qantio.sdk.public.models.dataconnector import Connector
    
@dataclass_json
class ExperimentResult(OperationResult):
    payload:json

class ExperimentVerbosity(Enum):
    SILENT      = 0
    MINIMAL     = 1
    NORMAL      = 2
    CHATTY      = 3
    MAXIMAL     = 4

class ExperimentJob(Enum):
    OUTLIERS    = 'OUTLIERS'
    ANALYSIS    = 'ANALYSIS'
    FORECAST    = 'FORECAST'
    BACKTEST    = 'BACKTEST'
    HYPERTUNE   = 'HYPERTUNE'

@dataclass_json
@dataclass
class ExperimentPool():
    client      : QantioClient
    experiments : list[Experiment]          = field(default_factory=list) 
    n_jobs      : int                       = 1
    result      : list[ExperimentResult]    = field(default_factory=list) 

    def validate(self)-> OperationResult:
        return OperationResult()

    async def run_async(self)->Experiment:
        await sleep(10)
        for exp in self.experiments:
            validation= exp.validate()
            if not validation.Success:
                pass
        
        self.result = []
        return Experiment

    def save_as_pipeline(self, client:QantioClient)->OperationResult:
        return OperationResult()

    async def save_async(self, destination:Connector)->OperationResult:
        await sleep(10)
        return OperationResult()

@dataclass_json
@dataclass
class ExperimentSettings():
    name            : str
    target_col      : str  
    job             : ExperimentJob     
    job_params      : dict                  = field(default_factory=dict) 
    job_id          : uuid                  = uuid.uuid4()
    verbosity       : ExperimentVerbosity   = ExperimentVerbosity.NORMAL

@dataclass_json
@dataclass
class Experiment():
    settings    : ExperimentSettings    = field(default_factory=ExperimentSettings) 
    time_serie  : 'TimeSerie'           = None
    result      : ExperimentResult      = None
    messages    : list                  = field(default_factory=list)

    def validate(self)-> OperationResult:
        return OperationResult()
    
    async def run_async(self, client:QantioClient)-> Experiment:
        await sleep(10)
        self.result=ExperimentResult()
        return self

    def run(self, client:QantioClient)-> Experiment:
        self.result = experiment_manager.run(self, client)
        return self

    def save_result(self, destination:'Connector')->OperationResult:
        return OperationResult()

    def save_as_pipeline(self, client:QantioClient)->OperationResult:
        return OperationResult()

    async def save_result_async(self, destination:'Connector')->OperationResult:
        await sleep(10)
        return OperationResult()


