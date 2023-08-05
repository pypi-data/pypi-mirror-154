from .const import CONF_API_ENABLED as CONF_API_ENABLED, CONF_PATH as CONF_PATH, CONF_PRODUCT_NAME as CONF_PRODUCT_NAME, CONF_PRODUCT_TYPE as CONF_PRODUCT_TYPE, CONF_SERIAL as CONF_SERIAL, DOMAIN as DOMAIN
from _typeshed import Incomplete
from homeassistant import config_entries as config_entries
from homeassistant.components import persistent_notification as persistent_notification, zeroconf as zeroconf
from homeassistant.const import CONF_IP_ADDRESS as CONF_IP_ADDRESS
from homeassistant.data_entry_flow import AbortFlow as AbortFlow, FlowResult as FlowResult
from typing import Any

_LOGGER: Incomplete

class ConfigFlow(config_entries.ConfigFlow):
    VERSION: int
    config: Incomplete
    def __init__(self) -> None: ...
    async def async_step_import(self, import_config: dict[str, Any]) -> FlowResult: ...
    async def async_step_user(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_zeroconf(self, discovery_info: zeroconf.ZeroconfServiceInfo) -> FlowResult: ...
    async def async_step_discovery_confirm(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    @staticmethod
    async def _async_try_connect_and_fetch(ip_address: str) -> dict[str, Any]: ...
    async def _async_set_and_check_unique_id(self, entry_info: dict[str, Any]) -> None: ...
