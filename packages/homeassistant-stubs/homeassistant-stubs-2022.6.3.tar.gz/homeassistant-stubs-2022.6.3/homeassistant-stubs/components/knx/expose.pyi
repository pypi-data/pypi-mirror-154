from .const import KNX_ADDRESS as KNX_ADDRESS
from .schema import ExposeSchema as ExposeSchema
from _typeshed import Incomplete
from collections.abc import Callable as Callable
from homeassistant.const import CONF_ENTITY_ID as CONF_ENTITY_ID, STATE_OFF as STATE_OFF, STATE_ON as STATE_ON, STATE_UNAVAILABLE as STATE_UNAVAILABLE, STATE_UNKNOWN as STATE_UNKNOWN
from homeassistant.core import Event as Event, HomeAssistant as HomeAssistant, State as State, callback as callback
from homeassistant.helpers.event import async_track_state_change_event as async_track_state_change_event
from homeassistant.helpers.typing import ConfigType as ConfigType, StateType as StateType
from xknx import XKNX as XKNX
from xknx.devices import DateTime, ExposeSensor

_LOGGER: Incomplete

def create_knx_exposure(hass: HomeAssistant, xknx: XKNX, config: ConfigType) -> Union[KNXExposeSensor, KNXExposeTime]: ...

class KNXExposeSensor:
    hass: Incomplete
    xknx: Incomplete
    type: Incomplete
    entity_id: Incomplete
    expose_attribute: Incomplete
    expose_default: Incomplete
    address: Incomplete
    _remove_listener: Incomplete
    device: Incomplete
    def __init__(self, hass: HomeAssistant, xknx: XKNX, expose_type: Union[int, str], entity_id: str, attribute: Union[str, None], default: StateType, address: str) -> None: ...
    def async_register(self) -> ExposeSensor: ...
    def _init_expose_state(self) -> None: ...
    def shutdown(self) -> None: ...
    def _get_expose_value(self, state: Union[State, None]) -> StateType: ...
    async def _async_entity_changed(self, event: Event) -> None: ...
    async def _async_set_knx_value(self, value: StateType) -> None: ...

class KNXExposeTime:
    xknx: Incomplete
    expose_type: Incomplete
    address: Incomplete
    device: Incomplete
    def __init__(self, xknx: XKNX, expose_type: str, address: str) -> None: ...
    def async_register(self) -> DateTime: ...
    def shutdown(self) -> None: ...
