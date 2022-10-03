from io import TextIOWrapper
from typing import Any, Dict, Literal

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

config: Dict[str, Any] = {}

# if config.yaml exists, read from config.yaml
CONFIG_YAML: Literal["config.yaml"] = "config.yaml"
_stream: TextIOWrapper = open(f"./{CONFIG_YAML}", mode="r", encoding="utf-8")
config = load(_stream, Loader=Loader)
