import logging
from dataclasses_json import dataclass_json
from typing import TYPE_CHECKING

#================================================================
import qantio.sdk.public.models.experiment as x
from qantio.sdk.public.client.qantio_client import QantioClient
from qantio.sdk.public.common.settings import qantio_settings
#================================================================

if TYPE_CHECKING:
    from qantio.sdk.public.models.experiment import Experiment, ExperimentResult

logger = logging.getLogger(__name__)

API_SETTINGS = qantio_settings()['api']['services']['experiment']

def run(experiment:'Experiment', client:QantioClient)->'ExperimentResult':
    
    experiment_result = x.ExperimentResult(
        OperationName = f"run experiment {experiment.settings.name} : <{experiment.settings.job_id}> with job <{experiment.settings.job}>")
    
    url = API_SETTINGS[str(experiment.settings.job.value).lower()]
    
    logger.info(f"{experiment.settings.name} > start")

    # response = client.http_client.post(
    #     url     = url, 
    #     json    = experiment.to_json(), 
    #     verify  = False
    # )

    # experiment_result.Success = (response.status_code==200)
    # experiment_result.experiment_result = response.json()
    
    # Dummy response
    
    experiment_result.Success = True
    experiment_result.payload = {'toto':1, 'titi':2}

    logger.log(11, f"{experiment.settings.name} > status > {experiment_result.Success}")
    logger.log(11, f"{experiment.settings.name} > payload > {experiment_result.payload}")

    return experiment_result.finalize()