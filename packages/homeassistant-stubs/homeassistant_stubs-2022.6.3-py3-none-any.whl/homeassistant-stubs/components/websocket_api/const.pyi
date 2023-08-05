from .connection import ActiveConnection as ActiveConnection
from _typeshed import Incomplete
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.json import JSONEncoder as JSONEncoder
from typing import Final

WebSocketCommandHandler: Incomplete
AsyncWebSocketCommandHandler: Incomplete
DOMAIN: Final[str]
URL: Final[str]
PENDING_MSG_PEAK: Final[int]
PENDING_MSG_PEAK_TIME: Final[int]
MAX_PENDING_MSG: Final[int]
ERR_ID_REUSE: Final[str]
ERR_INVALID_FORMAT: Final[str]
ERR_NOT_FOUND: Final[str]
ERR_NOT_SUPPORTED: Final[str]
ERR_HOME_ASSISTANT_ERROR: Final[str]
ERR_UNKNOWN_COMMAND: Final[str]
ERR_UNKNOWN_ERROR: Final[str]
ERR_UNAUTHORIZED: Final[str]
ERR_TIMEOUT: Final[str]
ERR_TEMPLATE_ERROR: Final[str]
TYPE_RESULT: Final[str]
CANCELLATION_ERRORS: Final[Incomplete]
SIGNAL_WEBSOCKET_CONNECTED: Final[str]
SIGNAL_WEBSOCKET_DISCONNECTED: Final[str]
DATA_CONNECTIONS: Final[Incomplete]
JSON_DUMP: Final[Incomplete]
COMPRESSED_STATE_STATE: str
COMPRESSED_STATE_ATTRIBUTES: str
COMPRESSED_STATE_CONTEXT: str
COMPRESSED_STATE_LAST_CHANGED: str
COMPRESSED_STATE_LAST_UPDATED: str
