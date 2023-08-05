from .const import DATA_CLIENT as DATA_CLIENT, DOMAIN as DOMAIN
from .discovery import ZwaveDiscoveryInfo as ZwaveDiscoveryInfo
from .discovery_data_template import FanValueMapping as FanValueMapping, FanValueMappingDataTemplate as FanValueMappingDataTemplate
from .entity import ZWaveBaseEntity as ZWaveBaseEntity
from .helpers import get_value_of_zwave_value as get_value_of_zwave_value
from _typeshed import Incomplete
from homeassistant.components.fan import FanEntity as FanEntity, FanEntityFeature as FanEntityFeature, NotValidPresetModeError as NotValidPresetModeError
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.util.percentage import int_states_in_range as int_states_in_range, percentage_to_ranged_value as percentage_to_ranged_value, ranged_value_to_percentage as ranged_value_to_percentage
from typing import Any
from zwave_js_server.model.driver import Driver as Driver
from zwave_js_server.model.value import Value as ZwaveValue

PARALLEL_UPDATES: int
DEFAULT_SPEED_RANGE: Incomplete
ATTR_FAN_STATE: str

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class ZwaveFan(ZWaveBaseEntity, FanEntity):
    _attr_supported_features: Incomplete
    _target_value: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    async def async_set_percentage(self, percentage: int) -> None: ...
    async def async_turn_on(self, percentage: Union[int, None] = ..., preset_mode: Union[str, None] = ..., **kwargs: Any) -> None: ...
    async def async_turn_off(self, **kwargs: Any) -> None: ...
    @property
    def is_on(self) -> Union[bool, None]: ...
    @property
    def percentage(self) -> Union[int, None]: ...
    @property
    def percentage_step(self) -> float: ...
    @property
    def speed_count(self) -> int: ...

class ValueMappingZwaveFan(ZwaveFan):
    data_template: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    async def async_set_percentage(self, percentage: int) -> None: ...
    async def async_set_preset_mode(self, preset_mode: str) -> None: ...
    @property
    def available(self) -> bool: ...
    @property
    def percentage(self) -> Union[int, None]: ...
    @property
    def percentage_step(self) -> float: ...
    @property
    def preset_modes(self) -> list[str]: ...
    @property
    def preset_mode(self) -> Union[str, None]: ...
    @property
    def has_fan_value_mapping(self) -> bool: ...
    @property
    def fan_value_mapping(self) -> FanValueMapping: ...
    @property
    def speed_count(self) -> int: ...
    @property
    def supported_features(self) -> int: ...
    def percentage_to_zwave_speed(self, percentage: int) -> int: ...
    def zwave_speed_to_percentage(self, zwave_speed: int) -> Union[int, None]: ...

class ZwaveThermostatFan(ZWaveBaseEntity, FanEntity):
    _fan_mode: ZwaveValue
    _fan_off: Union[ZwaveValue, None]
    _fan_state: Union[ZwaveValue, None]
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    async def async_turn_on(self, percentage: Union[int, None] = ..., preset_mode: Union[str, None] = ..., **kwargs: Any) -> None: ...
    async def async_turn_off(self, **kwargs: Any) -> None: ...
    @property
    def is_on(self) -> Union[bool, None]: ...
    @property
    def preset_mode(self) -> Union[str, None]: ...
    async def async_set_preset_mode(self, preset_mode: str) -> None: ...
    @property
    def preset_modes(self) -> Union[list[str], None]: ...
    @property
    def supported_features(self) -> int: ...
    @property
    def fan_state(self) -> Union[str, None]: ...
    @property
    def extra_state_attributes(self) -> Union[dict[str, str], None]: ...
