from ..helpers.frame import MissingIntegrationFrame as MissingIntegrationFrame, get_integration_frame as get_integration_frame
from collections.abc import Callable as Callable
from typing import Any

def deprecated_substitute(substitute_name: str) -> Callable[..., Callable]: ...
def get_deprecated(config: dict[str, Any], new_name: str, old_name: str, default: Union[Any, None] = ...) -> Union[Any, None]: ...
def deprecated_class(replacement: str) -> Any: ...
def deprecated_function(replacement: str) -> Callable[..., Callable]: ...
def _print_deprecation_warning(obj: Any, replacement: str, description: str) -> None: ...
