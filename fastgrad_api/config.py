from io import TextIOWrapper
from typing import Any

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

_stream: TextIOWrapper = open("config.yaml", "r", encoding="utf-8")
config: Any = load(_stream, Loader=Loader)
print(config)
