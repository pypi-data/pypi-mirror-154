
import logging
import os
import platform
import sys
import colorlog
from logging.handlers import RotatingFileHandler

from ..helpers.user_context import get_context, CONTEXT_PREFIX
from ..helpers.user_context import add_to_context
from ..common.settings import qantio_settings

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.log_exporter import AzureEventHandler
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

"""

    This fucker needs some serious polishing

"""
GLOBAL_SETTINGS = qantio_settings()
LOGGER_SETTINGS = GLOBAL_SETTINGS['logging']

DEFAULT_LOG_LEVEL = logging.DEBUG
CLOUD_ROLE = f"{GLOBAL_SETTINGS['sdk']['name']}.{GLOBAL_SETTINGS['sdk']['platform']}.{GLOBAL_SETTINGS['sdk']['version']}"

class ContextFilter(logging.Filter):
    def __init__(self, user_context):
        self.user_context = user_context
    def filter(self, record):
        record.user_context = self.user_context
        return True

def callback_function(envelope):
    envelope.tags['ai.cloud.role'] = CLOUD_ROLE
    envelope.data.baseData.properties['os_type'] = platform.system()
    return True

def initialize_logging():
    
    # add_to_context('apikey','')
    # add_to_context('user_id','')
    # add_to_context('user_name','')
    # add_to_context('user_email','')
    # add_to_context('user_machine',str({
    #     'os':os.name, 
    #     'system':platform.system(),
    #     'release':platform.release(),
    #     'version':platform.version(),
    #     'processor':platform.processor(),
    #     'python_build':platform.python_build()
    #     }))
    # add_to_context('user_python', sys.version)

    logging.addLevelName(logging.DEBUG + 1, 'SUCCESS')
    
    qantio_logger = logging.getLogger(LOGGER_SETTINGS['name'])
    qantio_logger.setLevel(LOGGER_SETTINGS['level'])
    qantio_logger.filters = []
    
    color_formatter = colorlog.ColoredFormatter(
        '{log_color} {asctime} : {levelname:>8s} > {name} > {message}', 
        style='{',
        log_colors={
		    'TRACE':    'white',
		    'DEBUG':    'black,,bg_white',
		    'INFO':     'cyan',
            'SUCCESS':  'green',
		    'WARNING':  'yellow',
		    'ERROR':    'red',
		    'CRITICAL': 'red,bg_white',
	    })

    if LOGGER_SETTINGS['std_out_handler'].get('enable'):
        
        cs_handler = logging.StreamHandler(sys.stdout)
        cs_handler.setLevel(LOGGER_SETTINGS['std_out_handler'].get('level'))
        cs_handler.setFormatter(color_formatter)
        qantio_logger.addHandler(cs_handler)
    
    if LOGGER_SETTINGS['rotating_file_handler'].get('enable'):
        
        fs_formatter = logging.Formatter('{asctime};{user_context};{levelname};{name};[{message}]', style='{',)
        fs_handler = RotatingFileHandler(filename='qantio.log', maxBytes=200000, backupCount=50)
        fs_handler.setLevel(LOGGER_SETTINGS['rotating_file_handler'].get('level'))
        fs_handler.setFormatter(fs_formatter)
        qantio_logger.addHandler(fs_handler)

    if LOGGER_SETTINGS['azure_telemetry_handler'].get('enable'):
        
        az_formater = logging.Formatter('{asctime} {levelname} {name} {message}', style='{',)
        az_handler = AzureLogHandler(
            connection_string='InstrumentationKey=5bd40b52-c29e-4470-b33c-cc6c9521c8a6;IngestionEndpoint=https://westeurope-5.in.applicationinsights.azure.com/;LiveEndpoint=https://westeurope.livediagnostics.monitor.azure.com/')
        
        az_handler.add_telemetry_processor(callback_function)
        az_handler.setLevel(LOGGER_SETTINGS['azure_telemetry_handler'].get('level'))
        az_handler.setFormatter(az_formater)
        qantio_logger.addHandler(az_handler)

    qantio_logger = set_filters(qantio_logger)

    qantio_logger.info("logging > started")


def set_filters(logger:logging.Logger):
    user_context = get_context()
    for h in logger.handlers:
        h.filters=[]
        h.addFilter(ContextFilter(user_context=user_context))
    return logger

def set_qantio_log_level(level: int):
    logging.getLogger(LOGGER_SETTINGS['name']).setLevel(level)

def enable_debug_logging():
    """Enables debug logging for the arthurai package.
    """
    set_qantio_log_level(logging.DEBUG)


def disable_debug_logging():
    """Disables debug logging for the arthurai package.
    """
    set_qantio_log_level(DEFAULT_LOG_LEVEL)