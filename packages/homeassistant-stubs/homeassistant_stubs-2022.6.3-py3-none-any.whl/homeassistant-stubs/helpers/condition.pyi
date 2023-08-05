from .sun import get_astral_event_date as get_astral_event_date
from .template import Template as Template
from .trace import TraceElement as TraceElement, trace_append_element as trace_append_element, trace_path as trace_path, trace_path_get as trace_path_get, trace_stack_cv as trace_stack_cv, trace_stack_pop as trace_stack_pop, trace_stack_push as trace_stack_push, trace_stack_top as trace_stack_top
from .typing import ConfigType as ConfigType, TemplateVarsType as TemplateVarsType
from _typeshed import Incomplete
from collections.abc import Callable, Container, Generator
from datetime import time as dt_time, timedelta
from homeassistant.components.sensor import SensorDeviceClass as SensorDeviceClass
from homeassistant.const import ATTR_DEVICE_CLASS as ATTR_DEVICE_CLASS, ATTR_GPS_ACCURACY as ATTR_GPS_ACCURACY, ATTR_LATITUDE as ATTR_LATITUDE, ATTR_LONGITUDE as ATTR_LONGITUDE, CONF_ABOVE as CONF_ABOVE, CONF_AFTER as CONF_AFTER, CONF_ATTRIBUTE as CONF_ATTRIBUTE, CONF_BEFORE as CONF_BEFORE, CONF_BELOW as CONF_BELOW, CONF_CONDITION as CONF_CONDITION, CONF_DEVICE_ID as CONF_DEVICE_ID, CONF_ENABLED as CONF_ENABLED, CONF_ENTITY_ID as CONF_ENTITY_ID, CONF_ID as CONF_ID, CONF_MATCH as CONF_MATCH, CONF_STATE as CONF_STATE, CONF_VALUE_TEMPLATE as CONF_VALUE_TEMPLATE, CONF_WEEKDAY as CONF_WEEKDAY, CONF_ZONE as CONF_ZONE, ENTITY_MATCH_ALL as ENTITY_MATCH_ALL, ENTITY_MATCH_ANY as ENTITY_MATCH_ANY, STATE_UNAVAILABLE as STATE_UNAVAILABLE, STATE_UNKNOWN as STATE_UNKNOWN, SUN_EVENT_SUNRISE as SUN_EVENT_SUNRISE, SUN_EVENT_SUNSET as SUN_EVENT_SUNSET, WEEKDAYS as WEEKDAYS
from homeassistant.core import HomeAssistant as HomeAssistant, State as State, callback as callback
from homeassistant.exceptions import ConditionError as ConditionError, ConditionErrorContainer as ConditionErrorContainer, ConditionErrorIndex as ConditionErrorIndex, ConditionErrorMessage as ConditionErrorMessage, HomeAssistantError as HomeAssistantError, TemplateError as TemplateError
from homeassistant.util.async_ import run_callback_threadsafe as run_callback_threadsafe
from typing import Any

ASYNC_FROM_CONFIG_FORMAT: str
FROM_CONFIG_FORMAT: str
VALIDATE_CONFIG_FORMAT: str
_LOGGER: Incomplete
INPUT_ENTITY_ID: Incomplete
ConditionCheckerType = Callable[[HomeAssistant, TemplateVarsType], bool]

def condition_trace_append(variables: TemplateVarsType, path: str) -> TraceElement: ...
def condition_trace_set_result(result: bool, **kwargs: Any) -> None: ...
def condition_trace_update_result(**kwargs: Any) -> None: ...
def trace_condition(variables: TemplateVarsType) -> Generator[TraceElement, None, None]: ...
def trace_condition_function(condition: ConditionCheckerType) -> ConditionCheckerType: ...
async def async_from_config(hass: HomeAssistant, config: ConfigType) -> ConditionCheckerType: ...
async def async_and_from_config(hass: HomeAssistant, config: ConfigType) -> ConditionCheckerType: ...
async def async_or_from_config(hass: HomeAssistant, config: ConfigType) -> ConditionCheckerType: ...
async def async_not_from_config(hass: HomeAssistant, config: ConfigType) -> ConditionCheckerType: ...
def numeric_state(hass: HomeAssistant, entity: Union[None, str, State], below: Union[float, str, None] = ..., above: Union[float, str, None] = ..., value_template: Union[Template, None] = ..., variables: TemplateVarsType = ...) -> bool: ...
def async_numeric_state(hass: HomeAssistant, entity: Union[None, str, State], below: Union[float, str, None] = ..., above: Union[float, str, None] = ..., value_template: Union[Template, None] = ..., variables: TemplateVarsType = ..., attribute: Union[str, None] = ...) -> bool: ...
def async_numeric_state_from_config(config: ConfigType) -> ConditionCheckerType: ...
def state(hass: HomeAssistant, entity: Union[None, str, State], req_state: Any, for_period: Union[timedelta, None] = ..., attribute: Union[str, None] = ...) -> bool: ...
def state_from_config(config: ConfigType) -> ConditionCheckerType: ...
def sun(hass: HomeAssistant, before: Union[str, None] = ..., after: Union[str, None] = ..., before_offset: Union[timedelta, None] = ..., after_offset: Union[timedelta, None] = ...) -> bool: ...
def sun_from_config(config: ConfigType) -> ConditionCheckerType: ...
def template(hass: HomeAssistant, value_template: Template, variables: TemplateVarsType = ...) -> bool: ...
def async_template(hass: HomeAssistant, value_template: Template, variables: TemplateVarsType = ..., trace_result: bool = ...) -> bool: ...
def async_template_from_config(config: ConfigType) -> ConditionCheckerType: ...
def time(hass: HomeAssistant, before: Union[dt_time, str, None] = ..., after: Union[dt_time, str, None] = ..., weekday: Union[None, str, Container[str]] = ...) -> bool: ...
def time_from_config(config: ConfigType) -> ConditionCheckerType: ...
def zone(hass: HomeAssistant, zone_ent: Union[None, str, State], entity: Union[None, str, State]) -> bool: ...
def zone_from_config(config: ConfigType) -> ConditionCheckerType: ...
async def async_device_from_config(hass: HomeAssistant, config: ConfigType) -> ConditionCheckerType: ...
async def async_trigger_from_config(hass: HomeAssistant, config: ConfigType) -> ConditionCheckerType: ...
def numeric_state_validate_config(hass: HomeAssistant, config: ConfigType) -> ConfigType: ...
def state_validate_config(hass: HomeAssistant, config: ConfigType) -> ConfigType: ...
async def async_validate_condition_config(hass: HomeAssistant, config: ConfigType) -> ConfigType: ...
async def async_validate_conditions_config(hass: HomeAssistant, conditions: list[ConfigType]) -> list[Union[ConfigType, Template]]: ...
def async_extract_entities(config: Union[ConfigType, Template]) -> set[str]: ...
def async_extract_devices(config: Union[ConfigType, Template]) -> set[str]: ...
