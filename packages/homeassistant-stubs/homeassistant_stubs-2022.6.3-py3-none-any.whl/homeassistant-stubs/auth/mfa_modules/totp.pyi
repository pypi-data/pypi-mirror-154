import voluptuous as vol
from . import MULTI_FACTOR_AUTH_MODULES as MULTI_FACTOR_AUTH_MODULES, MULTI_FACTOR_AUTH_MODULE_SCHEMA as MULTI_FACTOR_AUTH_MODULE_SCHEMA, MultiFactorAuthModule as MultiFactorAuthModule, SetupFlow as SetupFlow
from _typeshed import Incomplete
from homeassistant.auth.models import User as User
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.helpers.storage import Store as Store
from typing import Any

REQUIREMENTS: Incomplete
CONFIG_SCHEMA: Incomplete
STORAGE_VERSION: int
STORAGE_KEY: str
STORAGE_USERS: str
STORAGE_USER_ID: str
STORAGE_OTA_SECRET: str
INPUT_FIELD_CODE: str
DUMMY_SECRET: str

def _generate_qr_code(data: str) -> str: ...
def _generate_secret_and_qr_code(username: str) -> tuple[str, str, str]: ...

class TotpAuthModule(MultiFactorAuthModule):
    DEFAULT_TITLE: str
    MAX_RETRY_TIME: int
    _users: Incomplete
    _user_store: Incomplete
    _init_lock: Incomplete
    def __init__(self, hass: HomeAssistant, config: dict[str, Any]) -> None: ...
    @property
    def input_schema(self) -> vol.Schema: ...
    async def _async_load(self) -> None: ...
    async def _async_save(self) -> None: ...
    def _add_ota_secret(self, user_id: str, secret: Union[str, None] = ...) -> str: ...
    async def async_setup_flow(self, user_id: str) -> SetupFlow: ...
    async def async_setup_user(self, user_id: str, setup_data: Any) -> str: ...
    async def async_depose_user(self, user_id: str) -> None: ...
    async def async_is_user_setup(self, user_id: str) -> bool: ...
    async def async_validate(self, user_id: str, user_input: dict[str, Any]) -> bool: ...
    def _validate_2fa(self, user_id: str, code: str) -> bool: ...

class TotpSetupFlow(SetupFlow):
    _auth_module: Incomplete
    _user: Incomplete
    _ota_secret: str
    _url: Incomplete
    _image: Incomplete
    def __init__(self, auth_module: TotpAuthModule, setup_schema: vol.Schema, user: User) -> None: ...
    async def async_step_init(self, user_input: Union[dict[str, str], None] = ...) -> FlowResult: ...
