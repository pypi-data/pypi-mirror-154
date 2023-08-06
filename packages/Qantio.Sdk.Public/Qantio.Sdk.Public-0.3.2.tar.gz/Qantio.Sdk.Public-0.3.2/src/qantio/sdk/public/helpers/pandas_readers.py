import pandas as pd
import logging

logger = logging.getLogger("qantio.sdk.helpers.readers")

class reader:
    
    def adjust_settings(self, extension: str, settings: dict) -> dict:

        if extension == "feather":
            settings = {"path": settings["filepath_or_buffer"]}

        return settings

    def read(self, extension: str, **settings) -> pd.DataFrame:
        reader = "read_" + extension
        logger.info(f"Reading a {extension} object")
        reader_settings = self.adjust_settings(extension, settings)
        df = getattr(pd, reader)(**reader_settings)
        return df
