from .const import DATA_CLIENT as DATA_CLIENT, DOMAIN as DOMAIN
from .discovery import ZwaveDiscoveryInfo as ZwaveDiscoveryInfo
from .entity import ZWaveBaseEntity as ZWaveBaseEntity
from _typeshed import Incomplete
from homeassistant.components.number import NumberEntity as NumberEntity
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from zwave_js_server.model.driver import Driver as Driver
from zwave_js_server.model.value import Value as Value

PARALLEL_UPDATES: int

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class ZwaveNumberEntity(ZWaveBaseEntity, NumberEntity):
    _target_value: Incomplete
    _attr_name: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    @property
    def min_value(self) -> float: ...
    @property
    def max_value(self) -> float: ...
    @property
    def value(self) -> Union[float, None]: ...
    @property
    def unit_of_measurement(self) -> Union[str, None]: ...
    async def async_set_value(self, value: float) -> None: ...

class ZwaveVolumeNumberEntity(ZWaveBaseEntity, NumberEntity):
    correction_factor: Incomplete
    _attr_min_value: int
    _attr_max_value: int
    _attr_step: float
    _attr_name: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    @property
    def value(self) -> Union[float, None]: ...
    async def async_set_value(self, value: float) -> None: ...
