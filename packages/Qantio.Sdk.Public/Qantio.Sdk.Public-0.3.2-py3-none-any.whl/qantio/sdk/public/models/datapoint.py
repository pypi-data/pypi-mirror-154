from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import logging
import numbers
from typing import Callable, Dict, List, overload
from slugify import slugify
from datetime import datetime

from qantio.sdk.public.models.geography_point import GeographyPoint

logger = logging.getLogger(__name__)

class DataPoint:
    timestamp       : datetime           = datetime.now()
    dimensions      : dict[str, str]     = {}
    observations    : dict[str, float]   = {}
    exogenous       : dict[str, float]   = {}
    place           : GeographyPoint     = None

    def __init__(
        self, 
        timestamp           : datetime, 
        observation_name    : str, 
        observation_value   : float, 
        observations        : dict(str, float)  = {}, 
        dimensions          : dict(str, str)    = {}, 
        exogenous           : dict(str, float)  = {}, 
        place               : GeographyPoint    = None
        ):
        
        self.dimensions = {}
        self.observations = {}
        self.exogenous = {}
        self.place = None
        
        self.timestamp = timestamp
        
        if not observation_name is None and not observation_value is None:
            self = self.add_observation(observation_name, observation_value)
        
        self.set_place(place)

        for name, value in observations.items():
            self.add_observation(name, value)
        
        for name, value in dimensions.items():
            self.add_dimension(name, value)

        for name, value in exogenous.items():
            self.add_exogenous(name, value)
    
    def _add_property_to_collection(self, collection:dict, collection_type:str, name:str, value:any)->DataPoint:
        
        if not collection_type in ['obs_', 'dim_', 'exo_', 'prop_']:
            logger.warn(f"Invalid type")
            return self    

        if not name or name=="":
            logger.warn(f"Datapoint property was skipped because it has no name.")
            return self
        
        if name.startswith(collection_type):
            logger.warn(f"Datapoint property <{name}> was skipped because it has an invalid name. Starting with <{collection_type}>")
            return self

        if len(name)>59:
            logger.warn(f"Datapoint property <{name}> was skipped because it has an invalid name. <{name}> is too long. Rule : < 59")
            return self

        if value is None:
            logger.warn(f"Datapoint property <{name}> was skipped because it has no value.")
            return self

        if collection_type in ['obs_', 'exo_', 'prop_'] and not isinstance(value, numbers.Number):
            logger.warn(f"Datapoint property <{name}> was skipped because it is not a number.")
            return self

        if collection_type == 'dim_':
            value = str(value)
            if len(value)>256:
                logger.warn(f"Datapoint property <{name}> was skipped because its value is too long. Rule : < 256")
                return self
            
        property_name = f'{slugify(name, separator="_", stopwords=[collection_type])}' 
        property_key = collection_type + property_name.lower()

        if property_key==collection_type:
            logger.warn(f"Datapoint property <{name}> was skipped because it contains too many special chars.")
            return self

        if len(property_key)>59:
            logger.warn(f"Datapoint property <{property_key}> representing ({name}) was skipped because it's name is too long.")
            return self

        # if len(property_name)<=2:
        #     logger.info(f"Datapoint property <{name}> was kept but has low semantic value.")

        if property_key in collection.keys():
            logger.warn(f"Datapoint property <{name}> with value <{value}> was skipped because it is duplicated.")
            return self

        collection[property_key] = value

        return self

    def set_place(self, place:GeographyPoint)->DataPoint:
        self.place = place
        return self

    def add_observation(self, name:str, value:float)->DataPoint:
        return self._add_property_to_collection(
            collection      = self.observations,
            collection_type = "obs_",
            name            = name,
            value           = value
            )
    
    def add_exogenous(self, name:str, value:float)->DataPoint:
        return self._add_property_to_collection(
            collection      = self.exogenous,
            collection_type = "exo_",
            name            = name,
            value           = value
            )

    def add_dimension(self, name:str, value:str)->DataPoint:
        return self._add_property_to_collection(
            collection      = self.dimensions,
            collection_type = "dim_",
            name            = name,
            value           = value
            )