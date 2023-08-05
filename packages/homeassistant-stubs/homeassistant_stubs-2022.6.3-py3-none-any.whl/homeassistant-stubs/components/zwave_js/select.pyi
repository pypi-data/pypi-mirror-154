from .const import DATA_CLIENT as DATA_CLIENT, DOMAIN as DOMAIN
from .discovery import ZwaveDiscoveryInfo as ZwaveDiscoveryInfo
from .entity import ZWaveBaseEntity as ZWaveBaseEntity
from _typeshed import Incomplete
from homeassistant.components.select import SelectEntity as SelectEntity
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory as EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from zwave_js_server.model.driver import Driver as Driver

PARALLEL_UPDATES: int

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class ZwaveSelectEntity(ZWaveBaseEntity, SelectEntity):
    _attr_entity_category: Incomplete
    _attr_name: Incomplete
    _attr_options: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    @property
    def current_option(self) -> Union[str, None]: ...
    async def async_select_option(self, option: Union[str, int]) -> None: ...

class ZwaveDefaultToneSelectEntity(ZWaveBaseEntity, SelectEntity):
    _attr_entity_category: Incomplete
    _tones_value: Incomplete
    _attr_name: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    @property
    def options(self) -> list[str]: ...
    @property
    def current_option(self) -> Union[str, None]: ...
    async def async_select_option(self, option: Union[str, int]) -> None: ...

class ZwaveMultilevelSwitchSelectEntity(ZWaveBaseEntity, SelectEntity):
    _target_value: Incomplete
    _lookup_map: Incomplete
    _attr_options: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    @property
    def current_option(self) -> Union[str, None]: ...
    async def async_select_option(self, option: str) -> None: ...
