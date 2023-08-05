from . import CONF_NOISE_PSK as CONF_NOISE_PSK, DOMAIN as DOMAIN, DomainData as DomainData
from _typeshed import Incomplete
from aioesphomeapi import DeviceInfo as DeviceInfo
from homeassistant.components import zeroconf as zeroconf
from homeassistant.config_entries import ConfigFlow as ConfigFlow
from homeassistant.const import CONF_HOST as CONF_HOST, CONF_NAME as CONF_NAME, CONF_PASSWORD as CONF_PASSWORD, CONF_PORT as CONF_PORT
from homeassistant.core import callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from typing import Any

ERROR_REQUIRES_ENCRYPTION_KEY: str

class EsphomeFlowHandler(ConfigFlow):
    VERSION: int
    _host: Incomplete
    _port: Incomplete
    _password: Incomplete
    _noise_psk: Incomplete
    _device_info: Incomplete
    def __init__(self) -> None: ...
    async def _async_step_user_base(self, user_input: Union[dict[str, Any], None] = ..., error: Union[str, None] = ...) -> FlowResult: ...
    async def async_step_user(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_reauth(self, data: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_reauth_confirm(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    @property
    def _name(self) -> Union[str, None]: ...
    @_name.setter
    def _name(self, value: str) -> None: ...
    def _set_user_input(self, user_input: Union[dict[str, Any], None]) -> None: ...
    async def _async_try_fetch_device_info(self, user_input: Union[dict[str, Any], None]) -> FlowResult: ...
    async def _async_authenticate_or_add(self) -> FlowResult: ...
    async def async_step_discovery_confirm(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_zeroconf(self, discovery_info: zeroconf.ZeroconfServiceInfo) -> FlowResult: ...
    def _async_get_entry(self) -> FlowResult: ...
    async def async_step_encryption_key(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_authenticate(self, user_input: Union[dict[str, Any], None] = ..., error: Union[str, None] = ...) -> FlowResult: ...
    async def fetch_device_info(self) -> Union[str, None]: ...
    async def try_login(self) -> Union[str, None]: ...
