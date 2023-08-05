import datetime
from . import ATTR_LAST_RESET as ATTR_LAST_RESET, ATTR_STATE_CLASS as ATTR_STATE_CLASS, DOMAIN as DOMAIN, STATE_CLASSES as STATE_CLASSES, STATE_CLASS_MEASUREMENT as STATE_CLASS_MEASUREMENT, STATE_CLASS_TOTAL as STATE_CLASS_TOTAL, STATE_CLASS_TOTAL_INCREASING as STATE_CLASS_TOTAL_INCREASING, SensorDeviceClass as SensorDeviceClass
from _typeshed import Incomplete
from collections.abc import Callable as Callable, Iterable
from homeassistant.components.recorder import history as history, is_entity_recorded as is_entity_recorded, statistics as statistics
from homeassistant.components.recorder.models import StatisticData as StatisticData, StatisticMetaData as StatisticMetaData, StatisticResult as StatisticResult
from homeassistant.const import ATTR_DEVICE_CLASS as ATTR_DEVICE_CLASS, ATTR_UNIT_OF_MEASUREMENT as ATTR_UNIT_OF_MEASUREMENT, ENERGY_KILO_WATT_HOUR as ENERGY_KILO_WATT_HOUR, ENERGY_MEGA_WATT_HOUR as ENERGY_MEGA_WATT_HOUR, ENERGY_WATT_HOUR as ENERGY_WATT_HOUR, POWER_KILO_WATT as POWER_KILO_WATT, POWER_WATT as POWER_WATT, PRESSURE_BAR as PRESSURE_BAR, PRESSURE_HPA as PRESSURE_HPA, PRESSURE_INHG as PRESSURE_INHG, PRESSURE_KPA as PRESSURE_KPA, PRESSURE_MBAR as PRESSURE_MBAR, PRESSURE_PA as PRESSURE_PA, PRESSURE_PSI as PRESSURE_PSI, TEMP_CELSIUS as TEMP_CELSIUS, TEMP_FAHRENHEIT as TEMP_FAHRENHEIT, TEMP_KELVIN as TEMP_KELVIN, VOLUME_CUBIC_FEET as VOLUME_CUBIC_FEET, VOLUME_CUBIC_METERS as VOLUME_CUBIC_METERS
from homeassistant.core import HomeAssistant as HomeAssistant, State as State
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.entity import entity_sources as entity_sources
from sqlalchemy.orm.session import Session as Session
from typing import Any

_LOGGER: Incomplete
DEFAULT_STATISTICS: Incomplete
DEVICE_CLASS_UNITS: dict[str, str]
UNIT_CONVERSIONS: dict[str, dict[str, Callable]]
SEEN_DIP: str
WARN_DIP: str
WARN_NEGATIVE: str
WARN_UNSUPPORTED_UNIT: str
WARN_UNSTABLE_UNIT: str
LINK_DEV_STATISTICS: str

def _get_sensor_states(hass: HomeAssistant) -> list[State]: ...
def _time_weighted_average(fstates: list[tuple[float, State]], start: datetime.datetime, end: datetime.datetime) -> float: ...
def _get_units(fstates: list[tuple[float, State]]) -> set[Union[str, None]]: ...
def _parse_float(state: str) -> float: ...
def _normalize_states(hass: HomeAssistant, session: Session, old_metadatas: dict[str, tuple[int, StatisticMetaData]], entity_history: Iterable[State], device_class: Union[str, None], entity_id: str) -> tuple[Union[str, None], list[tuple[float, State]]]: ...
def _suggest_report_issue(hass: HomeAssistant, entity_id: str) -> str: ...
def warn_dip(hass: HomeAssistant, entity_id: str, state: State, previous_fstate: float) -> None: ...
def warn_negative(hass: HomeAssistant, entity_id: str, state: State) -> None: ...
def reset_detected(hass: HomeAssistant, entity_id: str, fstate: float, previous_fstate: Union[float, None], state: State) -> bool: ...
def _wanted_statistics(sensor_states: list[State]) -> dict[str, set[str]]: ...
def _last_reset_as_utc_isoformat(last_reset_s: Any, entity_id: str) -> Union[str, None]: ...
def compile_statistics(hass: HomeAssistant, start: datetime.datetime, end: datetime.datetime) -> statistics.PlatformCompiledStatistics: ...
def _compile_statistics(hass: HomeAssistant, session: Session, start: datetime.datetime, end: datetime.datetime) -> statistics.PlatformCompiledStatistics: ...
def list_statistic_ids(hass: HomeAssistant, statistic_ids: Union[list[str], tuple[str], None] = ..., statistic_type: Union[str, None] = ...) -> dict: ...
def validate_statistics(hass: HomeAssistant) -> dict[str, list[statistics.ValidationIssue]]: ...
