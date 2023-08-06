
import logging
import pkg_resources

SDK_NAME    = "Qantio.Sdk.Public"
SDK_VERSION = "0.2.8"

try:
    SDK_NAME    = pkg_resources.require("Qantio.Sdk.Public")[0].project_name 
    SDK_VERSION = pkg_resources.require("Qantio.Sdk.Public")[0].version 
except Exception:
    pass

def qantio_settings():
    """
        Base settings for qant.io public SDK

        Returns:
           JSON
    """
    return  {
        # DO NOT CHANGE
        "sdk":{
            "name"      : SDK_NAME,
            "platform"  : "python",
            "version"   : SDK_VERSION,
        },
        # DO NOT CHANGE
        "auth": {
            "application_scopes"        : ["https://qantioad.onmicrosoft.com/api-public/api.ingest.allow"],
            "application_clientid"      : "eb4c9d93-07a8-49e0-9d61-f22780fc149b",
            "application_b2c_authority" : "https://auth.qant.io/tfp/a03e474e-067b-4549-a7c7-cfe1c1d0469c/B2C_1_B2C_1A_ROPC_",
            "application_redirect_uri"  : "https://jwt.ms/",
        },
        # DO NOT CHANGE
        "api":{
            "base_address" : "https://api.qant.io",
            "services": {
                "experiment":{
                    "forecast"  : "/client/timeseries/experiment/forecast",
                    "backtest"  : "/client/timeseries/experiment/backtest",
                    "analysis"  : "/client/timeseries/experiment/analysis",
                    "hypertune" : "/client/timeseries/experiment/hypertune",
                    "outliers"  : "/client/timeseries/experiment/outliers",
                },
                "timeseries":{
                    "ingestion" : "/client/timeseries/ingestion/ingest",
                    "list"    : "/client/timeseries/manage/list",
                    "rename"    : "/client/timeseries/manage/rename",
                    "archive"   : "/client/timeseries/manage/archive",
                    "load"      : "/client/timeseries/data/load",
                    "infer"     : "/client/timeseries/inference/infer",
                    "forecast"  : "/client/timeseries/forecast/forecast",
                    "pipelines" : {
                        "list"      : "/client/timeseries/pipelines/list",
                        "one"      : "/client/timeseries/pipelines/one",
                        "start"     : "/client/timeseries/pipelines/start",
                        "stop"      : "/client/timeseries/pipelines/stop",
                        "archive"   : "/client/timeseries/pipelines/archive",
                        "delete"    : "/client/timeseries/pipelines/delete",
                        "create"    : "/client/timeseries/pipelines/create",
                        "run"       : "/client/timeseries/pipelines/run",
                    }
                }
            },
        },
        # YOU CAN CHANGE
        "logging": {
            "name"                      : "qantio", 
            "level"                     : logging.DEBUG, 
            "std_out_handler"           : {"enable":True, "level":logging.DEBUG},
            "azure_telemetry_handler"   : {"enable":True, "level":logging.INFO},
            "rotating_file_handler"     : {"enable":True, "level":logging.WARNING},
            }
}