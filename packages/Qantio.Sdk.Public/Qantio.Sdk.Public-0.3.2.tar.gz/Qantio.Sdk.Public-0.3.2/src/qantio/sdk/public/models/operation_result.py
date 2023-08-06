from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import List, Type

from dataclasses_json import dataclass_json

from qantio.sdk.public.models.batch_operation_result import BatchOperationResult

logger = logging.getLogger(__name__)

@dataclass_json
@dataclass(repr=True)
class OperationResult(object):
    OperationName       : str   = None
    Success             : bool  = False
    Outbound            : int   = 0
    Bytes               : int   = 0
    Errors              : list = field(default_factory=list)
    Exceptions          : list = field(default_factory=list)
    StartedAt           : datetime  = datetime.now()
    FinishedAt          : datetime  = datetime.now()
    Duration            : int       = 0
    Summary             : str       = None
    BatchOperations     : List[BatchOperationResult] = field(default_factory=list)

    def finalize(self, log_errors:bool=False)->OperationResult:

        self.Success    = not any(self.Errors) and not any([b for b in self.BatchOperations if not b.Success])
        self.FinishedAt = datetime.now()
        self.Duration   = (self.FinishedAt - self.StartedAt).total_seconds()
        
        if self.Outbound==0:
            self.Outbound = sum([b.DataPoints for b in self.BatchOperations if b.Success])
        
        if self.Bytes==0:
            self.Bytes = sum([b.BytesProcessed for b in self.BatchOperations if b.Success])
        
        if self.Success and self.Summary==None:
            self.Summary = f"Sent {self.Outbound} data points to the ingestion pipeline, with {self.Bytes} bytes with {len(self.BatchOperations)} batches in {self.Duration} ms."
        
        if log_errors:
            for e in self.Errors:
                logger.error(f"{self.OperationName} > {e}")

        return self