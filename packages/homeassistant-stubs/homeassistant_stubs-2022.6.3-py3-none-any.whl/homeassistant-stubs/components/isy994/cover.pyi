from .const import ISY994_NODES as ISY994_NODES, ISY994_PROGRAMS as ISY994_PROGRAMS, UOM_8_BIT_RANGE as UOM_8_BIT_RANGE, UOM_BARRIER as UOM_BARRIER, _LOGGER as _LOGGER
from .entity import ISYNodeEntity as ISYNodeEntity, ISYProgramEntity as ISYProgramEntity
from .helpers import migrate_old_unique_ids as migrate_old_unique_ids
from _typeshed import Incomplete
from homeassistant.components.cover import ATTR_POSITION as ATTR_POSITION, CoverEntity as CoverEntity, CoverEntityFeature as CoverEntityFeature
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from typing import Any

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class ISYCoverEntity(ISYNodeEntity, CoverEntity):
    _attr_supported_features: Incomplete
    @property
    def current_cover_position(self) -> Union[int, None]: ...
    @property
    def is_closed(self) -> Union[bool, None]: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
    async def async_set_cover_position(self, **kwargs: Any) -> None: ...

class ISYCoverProgramEntity(ISYProgramEntity, CoverEntity):
    @property
    def is_closed(self) -> bool: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
