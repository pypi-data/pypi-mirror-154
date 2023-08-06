from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

@dataclass(repr=True)
class BatchOperationResult(object):
    Success         : bool      = False
    Index           : int       = 0
    DataPoints      : int       = 0
    StartedAt       : datetime  = datetime.now()
    FinishedAt      : datetime  = datetime.now()
    StatusCode      : int       = 0
    ResponseHeaders : Dict      = field(default_factory=dict)
    ResponseErrors  : List[str] = field(default_factory=list)
    Duration        : float     = 0
    BytesProcessed  : int       = 0
    Summary         : str       = "Batch operation failed. Data may be partialy ingested."
    
    def finalize(self)->BatchOperationResult:
        
        self.Success    = not any(self.ResponseErrors)
        self.FinishedAt = datetime.now()
        self.Duration   = (self.FinishedAt - self.StartedAt).total_seconds()
       
        if self.Success:
            self.Summary = f"All went well for batch {self.Index}"

        return self
