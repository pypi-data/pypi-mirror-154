import voluptuous as vol
from . import ATTR_STATE_CLASS as ATTR_STATE_CLASS, DOMAIN as DOMAIN, SensorDeviceClass as SensorDeviceClass
from _typeshed import Incomplete
from homeassistant.components.automation import AutomationActionType as AutomationActionType, AutomationTriggerInfo as AutomationTriggerInfo
from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA as DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.device_automation.exceptions import InvalidDeviceAutomationConfig as InvalidDeviceAutomationConfig
from homeassistant.const import CONF_ABOVE as CONF_ABOVE, CONF_BELOW as CONF_BELOW, CONF_ENTITY_ID as CONF_ENTITY_ID, CONF_FOR as CONF_FOR, CONF_TYPE as CONF_TYPE
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.entity import get_capability as get_capability, get_device_class as get_device_class, get_unit_of_measurement as get_unit_of_measurement
from homeassistant.helpers.typing import ConfigType as ConfigType

DEVICE_CLASS_NONE: str
CONF_APPARENT_POWER: str
CONF_BATTERY_LEVEL: str
CONF_CO: str
CONF_CO2: str
CONF_CURRENT: str
CONF_ENERGY: str
CONF_FREQUENCY: str
CONF_GAS: str
CONF_HUMIDITY: str
CONF_ILLUMINANCE: str
CONF_NITROGEN_DIOXIDE: str
CONF_NITROGEN_MONOXIDE: str
CONF_NITROUS_OXIDE: str
CONF_OZONE: str
CONF_PM1: str
CONF_PM10: str
CONF_PM25: str
CONF_POWER: str
CONF_POWER_FACTOR: str
CONF_PRESSURE: str
CONF_REACTIVE_POWER: str
CONF_SIGNAL_STRENGTH: str
CONF_SULPHUR_DIOXIDE: str
CONF_TEMPERATURE: str
CONF_VOLATILE_ORGANIC_COMPOUNDS: str
CONF_VOLTAGE: str
CONF_VALUE: str
ENTITY_TRIGGERS: Incomplete
TRIGGER_SCHEMA: Incomplete

async def async_attach_trigger(hass: HomeAssistant, config: ConfigType, action: AutomationActionType, automation_info: AutomationTriggerInfo) -> CALLBACK_TYPE: ...
async def async_get_triggers(hass: HomeAssistant, device_id: str) -> list[dict[str, str]]: ...
async def async_get_trigger_capabilities(hass: HomeAssistant, config: ConfigType) -> dict[str, vol.Schema]: ...
