import yaml
from .objects import Input as Input, NodeListClass as NodeListClass
from _typeshed import Incomplete

def dump(_dict: dict) -> str: ...
def save_yaml(path: str, data: dict) -> None: ...
def represent_odict(dumper, tag, mapping, flow_style: Incomplete | None = ...) -> yaml.MappingNode: ...
