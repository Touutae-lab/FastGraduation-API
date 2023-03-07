import multiprocessing
from typing import Literal

bind: Literal["0.0.0.0:8000"] = "0.0.0.0:8000"
workers: int = multiprocessing.cpu_count() * 2 + 1
