from . import RainMachineEntity as RainMachineEntity
from .const import DATA_CONTROLLER as DATA_CONTROLLER, DATA_COORDINATOR as DATA_COORDINATOR, DATA_PROVISION_SETTINGS as DATA_PROVISION_SETTINGS, DATA_RESTRICTIONS_CURRENT as DATA_RESTRICTIONS_CURRENT, DATA_RESTRICTIONS_UNIVERSAL as DATA_RESTRICTIONS_UNIVERSAL, DOMAIN as DOMAIN
from .model import RainMachineDescriptionMixinApiCategory as RainMachineDescriptionMixinApiCategory
from .util import key_exists as key_exists
from _typeshed import Incomplete
from homeassistant.components.binary_sensor import BinarySensorEntity as BinarySensorEntity, BinarySensorEntityDescription as BinarySensorEntityDescription
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.entity import EntityCategory as EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback

TYPE_FLOW_SENSOR: str
TYPE_FREEZE: str
TYPE_FREEZE_PROTECTION: str
TYPE_HOT_DAYS: str
TYPE_HOURLY: str
TYPE_MONTH: str
TYPE_RAINDELAY: str
TYPE_RAINSENSOR: str
TYPE_WEEKDAY: str

class RainMachineBinarySensorDescription(BinarySensorEntityDescription, RainMachineDescriptionMixinApiCategory):
    def __init__(self, api_category, data_key, key, device_class, entity_category, entity_registry_enabled_default, entity_registry_visible_default, force_update, icon, name, unit_of_measurement) -> None: ...

BINARY_SENSOR_DESCRIPTIONS: Incomplete

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class CurrentRestrictionsBinarySensor(RainMachineEntity, BinarySensorEntity):
    _attr_is_on: Incomplete
    def update_from_latest_data(self) -> None: ...

class ProvisionSettingsBinarySensor(RainMachineEntity, BinarySensorEntity):
    _attr_is_on: Incomplete
    def update_from_latest_data(self) -> None: ...

class UniversalRestrictionsBinarySensor(RainMachineEntity, BinarySensorEntity):
    _attr_is_on: Incomplete
    def update_from_latest_data(self) -> None: ...
