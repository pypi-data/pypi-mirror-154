from .frame import report as report
from .storage import Store as Store
from .typing import UNDEFINED as UNDEFINED, UndefinedType as UndefinedType
from _typeshed import Incomplete
from collections.abc import Container, Iterable
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.loader import bind_hass as bind_hass
from homeassistant.util import slugify as slugify

DATA_REGISTRY: str
EVENT_AREA_REGISTRY_UPDATED: str
STORAGE_KEY: str
STORAGE_VERSION: int
SAVE_DELAY: int

class AreaEntry:
    name: str
    normalized_name: str
    picture: Union[str, None]
    id: Union[str, None]
    def generate_id(self, existing_ids: Container[str]) -> None: ...
    def __init__(self, name, normalized_name, picture, id) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

class AreaRegistry:
    hass: Incomplete
    areas: Incomplete
    _store: Incomplete
    _normalized_name_area_idx: Incomplete
    def __init__(self, hass: HomeAssistant) -> None: ...
    def async_get_area(self, area_id: str) -> Union[AreaEntry, None]: ...
    def async_get_area_by_name(self, name: str) -> Union[AreaEntry, None]: ...
    def async_list_areas(self) -> Iterable[AreaEntry]: ...
    def async_get_or_create(self, name: str) -> AreaEntry: ...
    def async_create(self, name: str, picture: Union[str, None] = ...) -> AreaEntry: ...
    def async_delete(self, area_id: str) -> None: ...
    def async_update(self, area_id: str, name: Union[str, UndefinedType] = ..., picture: Union[str, None, UndefinedType] = ...) -> AreaEntry: ...
    def _async_update(self, area_id: str, name: Union[str, UndefinedType] = ..., picture: Union[str, None, UndefinedType] = ...) -> AreaEntry: ...
    async def async_load(self) -> None: ...
    def async_schedule_save(self) -> None: ...
    def _data_to_save(self) -> dict[str, list[dict[str, Union[str, None]]]]: ...

def async_get(hass: HomeAssistant) -> AreaRegistry: ...
async def async_load(hass: HomeAssistant) -> None: ...
async def async_get_registry(hass: HomeAssistant) -> AreaRegistry: ...
def normalize_area_name(area_name: str) -> str: ...
