from .const import DOMAIN as DOMAIN, SIG_CROWNSTONE_STATE_UPDATE as SIG_CROWNSTONE_STATE_UPDATE, SIG_UART_STATE_CHANGE as SIG_UART_STATE_CHANGE, SSE_LISTENERS as SSE_LISTENERS, UART_LISTENERS as UART_LISTENERS
from .entry_manager import CrownstoneEntryManager as CrownstoneEntryManager
from crownstone_core.packets.serviceDataParsers.containers.AdvExternalCrownstoneState import AdvExternalCrownstoneState as AdvExternalCrownstoneState
from crownstone_sse.events import AbilityChangeEvent as AbilityChangeEvent, SwitchStateUpdateEvent as SwitchStateUpdateEvent
from homeassistant.core import callback as callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect, async_dispatcher_send as async_dispatcher_send, dispatcher_send as dispatcher_send

def async_update_crwn_state_sse(manager: CrownstoneEntryManager, switch_event: SwitchStateUpdateEvent) -> None: ...
def async_update_crwn_ability(manager: CrownstoneEntryManager, ability_event: AbilityChangeEvent) -> None: ...
def update_uart_state(manager: CrownstoneEntryManager, _: Union[bool, None]) -> None: ...
def update_crwn_state_uart(manager: CrownstoneEntryManager, data: AdvExternalCrownstoneState) -> None: ...
def setup_sse_listeners(manager: CrownstoneEntryManager) -> None: ...
def setup_uart_listeners(manager: CrownstoneEntryManager) -> None: ...
