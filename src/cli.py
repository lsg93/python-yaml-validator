from dataclasses import dataclass
from typing import Optional


# This class hasn't got any actual usage at the moment, it's just a foundation to get tests passing.
@dataclass
class Config:
    path: Optional[str] = None
