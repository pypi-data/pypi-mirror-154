from . import DOMAIN as DOMAIN
from .deconz_event import CONF_DECONZ_EVENT as CONF_DECONZ_EVENT, CONF_GESTURE as CONF_GESTURE, DeconzAlarmEvent as DeconzAlarmEvent, DeconzEvent as DeconzEvent
from .gateway import DeconzGateway as DeconzGateway
from _typeshed import Incomplete
from homeassistant.components.automation import AutomationActionType as AutomationActionType, AutomationTriggerInfo as AutomationTriggerInfo
from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA as DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.device_automation.exceptions import InvalidDeviceAutomationConfig as InvalidDeviceAutomationConfig
from homeassistant.const import CONF_DEVICE_ID as CONF_DEVICE_ID, CONF_DOMAIN as CONF_DOMAIN, CONF_EVENT as CONF_EVENT, CONF_PLATFORM as CONF_PLATFORM, CONF_TYPE as CONF_TYPE, CONF_UNIQUE_ID as CONF_UNIQUE_ID
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, HomeAssistant as HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.typing import ConfigType as ConfigType

CONF_SUBTYPE: str
CONF_SHORT_PRESS: str
CONF_SHORT_RELEASE: str
CONF_LONG_PRESS: str
CONF_LONG_RELEASE: str
CONF_DOUBLE_PRESS: str
CONF_TRIPLE_PRESS: str
CONF_QUADRUPLE_PRESS: str
CONF_QUINTUPLE_PRESS: str
CONF_ROTATED: str
CONF_ROTATED_FAST: str
CONF_ROTATION_STOPPED: str
CONF_AWAKE: str
CONF_MOVE: str
CONF_DOUBLE_TAP: str
CONF_SHAKE: str
CONF_FREE_FALL: str
CONF_FLIP_90: str
CONF_FLIP_180: str
CONF_MOVE_ANY: str
CONF_DOUBLE_TAP_ANY: str
CONF_TURN_CW: str
CONF_TURN_CCW: str
CONF_ROTATE_FROM_SIDE_1: str
CONF_ROTATE_FROM_SIDE_2: str
CONF_ROTATE_FROM_SIDE_3: str
CONF_ROTATE_FROM_SIDE_4: str
CONF_ROTATE_FROM_SIDE_5: str
CONF_ROTATE_FROM_SIDE_6: str
CONF_TURN_ON: str
CONF_TURN_OFF: str
CONF_DIM_UP: str
CONF_DIM_DOWN: str
CONF_LEFT: str
CONF_RIGHT: str
CONF_OPEN: str
CONF_CLOSE: str
CONF_BOTH_BUTTONS: str
CONF_TOP_BUTTONS: str
CONF_BOTTOM_BUTTONS: str
CONF_BUTTON_1: str
CONF_BUTTON_2: str
CONF_BUTTON_3: str
CONF_BUTTON_4: str
CONF_BUTTON_5: str
CONF_BUTTON_6: str
CONF_BUTTON_7: str
CONF_BUTTON_8: str
CONF_SIDE_1: str
CONF_SIDE_2: str
CONF_SIDE_3: str
CONF_SIDE_4: str
CONF_SIDE_5: str
CONF_SIDE_6: str
HUE_DIMMER_REMOTE_MODEL_GEN1: str
HUE_DIMMER_REMOTE_MODEL_GEN2: str
HUE_DIMMER_REMOTE_MODEL_GEN3: str
HUE_DIMMER_REMOTE: Incomplete
HUE_BUTTON_REMOTE_MODEL: str
HUE_BUTTON_REMOTE: Incomplete
HUE_TAP_REMOTE_MODEL: str
HUE_TAP_REMOTE: Incomplete
FRIENDS_OF_HUE_SWITCH_MODEL: str
FRIENDS_OF_HUE_SWITCH: Incomplete
STYRBAR_REMOTE_MODEL: str
STYRBAR_REMOTE: Incomplete
SYMFONISK_SOUND_CONTROLLER_MODEL: str
SYMFONISK_SOUND_CONTROLLER: Incomplete
TRADFRI_ON_OFF_SWITCH_MODEL: str
TRADFRI_ON_OFF_SWITCH: Incomplete
TRADFRI_OPEN_CLOSE_REMOTE_MODEL: str
TRADFRI_OPEN_CLOSE_REMOTE: Incomplete
TRADFRI_REMOTE_MODEL: str
TRADFRI_REMOTE: Incomplete
TRADFRI_SHORTCUT_REMOTE_MODEL: str
TRADFRI_SHORTCUT_REMOTE: Incomplete
TRADFRI_WIRELESS_DIMMER_MODEL: str
TRADFRI_WIRELESS_DIMMER: Incomplete
AQARA_CUBE_MODEL: str
AQARA_CUBE_MODEL_ALT1: str
AQARA_CUBE: Incomplete
AQARA_DOUBLE_WALL_SWITCH_MODEL: str
AQARA_DOUBLE_WALL_SWITCH_MODEL_2020: str
AQARA_DOUBLE_WALL_SWITCH: Incomplete
AQARA_DOUBLE_WALL_SWITCH_WXKG02LM_MODEL: str
AQARA_DOUBLE_WALL_SWITCH_WXKG02LM: Incomplete
AQARA_DOUBLE_WALL_SWITCH_QBKG12LM_MODEL: str
AQARA_DOUBLE_WALL_SWITCH_QBKG12LM: Incomplete
AQARA_SINGLE_WALL_SWITCH_QBKG11LM_MODEL: str
AQARA_SINGLE_WALL_SWITCH_QBKG11LM: Incomplete
AQARA_SINGLE_WALL_SWITCH_WXKG03LM_MODEL: str
AQARA_SINGLE_WALL_SWITCH_WXKG06LM_MODEL: str
AQARA_SINGLE_WALL_SWITCH: Incomplete
AQARA_MINI_SWITCH_MODEL: str
AQARA_MINI_SWITCH: Incomplete
AQARA_ROUND_SWITCH_MODEL: str
AQARA_ROUND_SWITCH: Incomplete
AQARA_SQUARE_SWITCH_MODEL: str
AQARA_SQUARE_SWITCH: Incomplete
AQARA_SQUARE_SWITCH_WXKG11LM_2016_MODEL: str
AQARA_SQUARE_SWITCH_WXKG11LM_2016: Incomplete
AQARA_OPPLE_2_BUTTONS_MODEL: str
AQARA_OPPLE_2_BUTTONS: Incomplete
AQARA_OPPLE_4_BUTTONS_MODEL: str
AQARA_OPPLE_4_BUTTONS: Incomplete
AQARA_OPPLE_6_BUTTONS_MODEL: str
AQARA_OPPLE_6_BUTTONS: Incomplete
DRESDEN_ELEKTRONIK_LIGHTING_SWITCH_MODEL: str
DRESDEN_ELEKTRONIK_LIGHTING_SWITCH: Incomplete
DRESDEN_ELEKTRONIK_SCENE_SWITCH_MODEL: str
DRESDEN_ELEKTRONIK_SCENE_SWITCH: Incomplete
GIRA_JUNG_SWITCH_MODEL: str
GIRA_SWITCH_MODEL: str
JUNG_SWITCH_MODEL: str
GIRA_JUNG_SWITCH: Incomplete
LEGRAND_ZGP_TOGGLE_SWITCH_MODEL: str
LEGRAND_ZGP_TOGGLE_SWITCH: Incomplete
LEGRAND_ZGP_SCENE_SWITCH_MODEL: str
LEGRAND_ZGP_SCENE_SWITCH: Incomplete
LIDL_SILVERCREST_DOORBELL_MODEL: str
LIDL_SILVERCREST_DOORBELL: Incomplete
LIGHTIFIY_FOUR_BUTTON_REMOTE_MODEL: str
LIGHTIFIY_FOUR_BUTTON_REMOTE_4X_MODEL: str
LIGHTIFIY_FOUR_BUTTON_REMOTE_4X_EU_MODEL: str
LIGHTIFIY_FOUR_BUTTON_REMOTE: Incomplete
BUSCH_JAEGER_REMOTE_1_MODEL: str
BUSCH_JAEGER_REMOTE_2_MODEL: str
BUSCH_JAEGER_REMOTE: Incomplete
SONOFF_SNZB_01_1_MODEL: str
SONOFF_SNZB_01_2_MODEL: str
SONOFF_SNZB_01_SWITCH: Incomplete
TRUST_ZYCT_202_MODEL: str
TRUST_ZYCT_202_ZLL_MODEL: str
TRUST_ZYCT_202: Incomplete
UBISYS_POWER_SWITCH_S2_MODEL: str
UBISYS_POWER_SWITCH_S2: Incomplete
UBISYS_CONTROL_UNIT_C4_MODEL: str
UBISYS_CONTROL_UNIT_C4: Incomplete
REMOTES: Incomplete
TRIGGER_SCHEMA: Incomplete

def _get_deconz_event_from_device(hass: HomeAssistant, device: dr.DeviceEntry) -> Union[DeconzAlarmEvent, DeconzEvent]: ...
async def async_validate_trigger_config(hass: HomeAssistant, config: ConfigType) -> ConfigType: ...
async def async_attach_trigger(hass: HomeAssistant, config: ConfigType, action: AutomationActionType, automation_info: AutomationTriggerInfo) -> CALLBACK_TYPE: ...
async def async_get_triggers(hass: HomeAssistant, device_id: str) -> list[dict[str, str]]: ...
