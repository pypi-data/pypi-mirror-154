import logging.handlers
from _typeshed import Incomplete
from collections.abc import Callable, Coroutine
from homeassistant.const import EVENT_HOMEASSISTANT_CLOSE as EVENT_HOMEASSISTANT_CLOSE
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback, is_callback as is_callback
from typing import Any, TypeVar, overload

_T = TypeVar('_T')

class HideSensitiveDataFilter(logging.Filter):
    text: Incomplete
    def __init__(self, text: str) -> None: ...
    def filter(self, record: logging.LogRecord) -> bool: ...

class HomeAssistantQueueHandler(logging.handlers.QueueHandler):
    def prepare(self, record: logging.LogRecord) -> logging.LogRecord: ...
    def handle(self, record: logging.LogRecord) -> Any: ...

def async_activate_log_queue_handler(hass: HomeAssistant) -> None: ...
def log_exception(format_err: Callable[..., Any], *args: Any) -> None: ...
@overload
def catch_log_exception(func: Callable[..., Coroutine[Any, Any, Any]], format_err: Callable[..., Any], *args: Any) -> Callable[..., Coroutine[Any, Any, None]]: ...
@overload
def catch_log_exception(func: Callable[..., Any], format_err: Callable[..., Any], *args: Any) -> Callable[..., Union[None, Coroutine[Any, Any, None]]]: ...
def catch_log_coro_exception(target: Coroutine[Any, Any, _T], format_err: Callable[..., Any], *args: Any) -> Coroutine[Any, Any, Union[_T, None]]: ...
def async_create_catching_coro(target: Coroutine[Any, Any, _T]) -> Coroutine[Any, Any, Union[_T, None]]: ...
