import logging
from typing import List
from public.client.qantio_client import QantioClient
from public.common.settings import qantio_settings
from public.models.experiment import Experiment, ExperimentResult
from dataclasses_json import dataclass_json

logger = logging.getLogger(__name__)

GLOBAL_SETTINGS = qantio_settings()
SERVICE = 'experiment'
API_SETTINGS = GLOBAL_SETTINGS['api']['services'][SERVICE]

def run_experiment(experiment:Experiment, client:QantioClient)->ExperimentResult:
    
    experiment_result = ExperimentResult(
        OperationName = f"run experiment id {experiment.settings.job_id} with job {experiment.settings.job}")
    
    url = API_SETTINGS[str(experiment.settings.job).lower()]
    
    print(url)
    print(experiment.to_json())
 
    # response = client.http_client.post(
    #     url     = url, 
    #     json    = experiment.to_json(), 
    #     verify  = False
    # )

    # experiment_result.Success = (response.status_code==200)
    # experiment_result.experiment_result = response.json()
    
    # Dummy respoonse
    experiment_result.Success = True
    experiment_result.experiment_result = {'toto':1, 'titi':2}
    print(experiment_result.to_json())
    
    return experiment_result.finalize()