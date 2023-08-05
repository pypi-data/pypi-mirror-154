import abc
import voluptuous as vol
from . import DEVICE_TRIGGER_BASE_SCHEMA as DEVICE_TRIGGER_BASE_SCHEMA, DeviceAutomationType as DeviceAutomationType, async_get_device_automation_platform as async_get_device_automation_platform
from .exceptions import InvalidDeviceAutomationConfig as InvalidDeviceAutomationConfig
from _typeshed import Incomplete
from collections.abc import Awaitable
from homeassistant.components.automation import AutomationActionType as AutomationActionType, AutomationTriggerInfo as AutomationTriggerInfo
from homeassistant.const import CONF_DOMAIN as CONF_DOMAIN
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, HomeAssistant as HomeAssistant
from homeassistant.helpers.typing import ConfigType as ConfigType
from typing import Any

TRIGGER_SCHEMA: Incomplete

class DeviceAutomationTriggerProtocol(metaclass=abc.ABCMeta):
    TRIGGER_SCHEMA: vol.Schema
    async def async_validate_trigger_config(self, hass: HomeAssistant, config: ConfigType) -> ConfigType: ...
    async def async_attach_trigger(self, hass: HomeAssistant, config: ConfigType, action: AutomationActionType, automation_info: AutomationTriggerInfo) -> CALLBACK_TYPE: ...
    def async_get_trigger_capabilities(self, hass: HomeAssistant, config: ConfigType) -> Union[dict[str, vol.Schema], Awaitable[dict[str, vol.Schema]]]: ...
    def async_get_triggers(self, hass: HomeAssistant, device_id: str) -> Union[list[dict[str, Any]], Awaitable[list[dict[str, Any]]]]: ...

async def async_validate_trigger_config(hass: HomeAssistant, config: ConfigType) -> ConfigType: ...
async def async_attach_trigger(hass: HomeAssistant, config: ConfigType, action: AutomationActionType, automation_info: AutomationTriggerInfo) -> CALLBACK_TYPE: ...
