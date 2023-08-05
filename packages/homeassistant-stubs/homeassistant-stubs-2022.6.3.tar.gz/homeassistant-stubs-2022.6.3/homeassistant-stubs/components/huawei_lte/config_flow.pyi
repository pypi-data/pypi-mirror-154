from .const import CONF_TRACK_WIRED_CLIENTS as CONF_TRACK_WIRED_CLIENTS, CONF_UNAUTHENTICATED_MODE as CONF_UNAUTHENTICATED_MODE, CONNECTION_TIMEOUT as CONNECTION_TIMEOUT, DEFAULT_DEVICE_NAME as DEFAULT_DEVICE_NAME, DEFAULT_NOTIFY_SERVICE_NAME as DEFAULT_NOTIFY_SERVICE_NAME, DEFAULT_TRACK_WIRED_CLIENTS as DEFAULT_TRACK_WIRED_CLIENTS, DEFAULT_UNAUTHENTICATED_MODE as DEFAULT_UNAUTHENTICATED_MODE, DOMAIN as DOMAIN
from .utils import get_device_macs as get_device_macs
from _typeshed import Incomplete
from homeassistant import config_entries as config_entries
from homeassistant.components import ssdp as ssdp
from homeassistant.const import CONF_MAC as CONF_MAC, CONF_NAME as CONF_NAME, CONF_PASSWORD as CONF_PASSWORD, CONF_RECIPIENT as CONF_RECIPIENT, CONF_URL as CONF_URL, CONF_USERNAME as CONF_USERNAME
from homeassistant.core import callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from huawei_lte_api.Session import GetResponseType as GetResponseType
from typing import Any

_LOGGER: Incomplete

class ConfigFlowHandler(config_entries.ConfigFlow):
    VERSION: int
    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlowHandler: ...
    async def _async_show_user_form(self, user_input: Union[dict[str, Any], None] = ..., errors: Union[dict[str, str], None] = ...) -> FlowResult: ...
    async def async_step_user(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_ssdp(self, discovery_info: ssdp.SsdpServiceInfo) -> FlowResult: ...

class OptionsFlowHandler(config_entries.OptionsFlow):
    config_entry: Incomplete
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None: ...
    async def async_step_init(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
