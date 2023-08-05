from .models import DSMRSensorEntityDescription as DSMRSensorEntityDescription
from _typeshed import Incomplete
from homeassistant.components.sensor import SensorDeviceClass as SensorDeviceClass, SensorStateClass as SensorStateClass
from homeassistant.const import Platform as Platform
from homeassistant.helpers.entity import EntityCategory as EntityCategory

DOMAIN: str
LOGGER: Incomplete
PLATFORMS: Incomplete
CONF_DSMR_VERSION: str
CONF_PROTOCOL: str
CONF_RECONNECT_INTERVAL: str
CONF_PRECISION: str
CONF_TIME_BETWEEN_UPDATE: str
CONF_SERIAL_ID: str
CONF_SERIAL_ID_GAS: str
DEFAULT_DSMR_VERSION: str
DEFAULT_PORT: str
DEFAULT_PRECISION: int
DEFAULT_RECONNECT_INTERVAL: int
DEFAULT_TIME_BETWEEN_UPDATE: int
DATA_TASK: str
DEVICE_NAME_ELECTRICITY: str
DEVICE_NAME_GAS: str
DSMR_VERSIONS: Incomplete
DSMR_PROTOCOL: str
RFXTRX_DSMR_PROTOCOL: str
SENSORS: tuple[DSMRSensorEntityDescription, ...]
