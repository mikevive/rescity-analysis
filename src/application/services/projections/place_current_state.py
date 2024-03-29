from abc import ABCMeta, abstractmethod
from typing import List

from application.services.dtos.place_created_dto import PlaceCreatedDto
from application.services.projections._projection import Projection
from application.services.dtos.event_dto import EventDto

class AlarmConfig:

  def __init__(self, activation: str, setpoint: float, alarm_id: str) -> None:
    self._activation: str = activation
    self._setpoint: int = setpoint
    self._alarm_id: str = alarm_id

  def get_activation(self) -> str:
    return self._activation

  def set_activation(self, activation: str) -> None:
    self._activation = activation

  def get_setpoint(self) -> float:
    return self._setpoint

  def set_setpoint(self, setpoint: float) -> None:
    self._setpoint = setpoint

  def get_alarm_id(self) -> str:
    return self._alarm_id

  def set_alarm_id(self, alarm_id: str) -> None:
    self._alarm_id = alarm_id

class Constant:

  def __init__(self, name: str, value: float) -> None:
    self._name: str = name
    self._value: int = value

  def get_name(self) -> str:
    return self._name

  def set_name(self, name: str) -> None:
    self._name = name

  def get_value(self) -> float:
    return self._value

  def set_value(self, value: float) -> None:
    self._value = value


class KpiConfig:

  def __init__(self, kpi_id: str, sensor_id: str, measurement: str, constants: List[Constant] = None, alarms_config: List[AlarmConfig] = None) -> None:
    self._kpi_id: str = kpi_id
    self._sensor_id: str = sensor_id
    self._measurement: str = measurement
    self._constants: List[Constant] = constants or []
    self._alarms_config: List[AlarmConfig] = alarms_config or []

  def get_kpi_id(self) -> str:
    return self._kpi_id

  def get_sensor_id(self) -> str:
    return self._sensor_id

  def get_measurement(self) -> str:
    return self._measurement

  def get_constants(self) -> List[Constant]:
    return self._constants

  def get_alarms_config(self) -> List[Constant]:
    return self._alarms_config

  def set_sensor_id(self, sensor_id: str) -> None:
    self._sensor_id = sensor_id

  def set_measurement(self, measurement: str) -> None:
    self._measurement = measurement

  def set_constants(self, constants: List[Constant]) -> None:
    self._constants = constants

  def set_alarms_config(self, alarms_config: List[AlarmConfig]) -> None:
    self._alarms_config = alarms_config


class KpiGroupConfig:

  def __init__(self, kpi_group_id: str, kpis_config: List[KpiConfig] = None) -> None:
    self._kpi_group_id: str = kpi_group_id
    self._kpis_config: List[KpiConfig] = kpis_config or []

  def get_kpi_group_id(self) -> str:
    return self._kpi_group_id

  def get_kpis_config(self) -> List[KpiConfig]:
    return self._kpis_config

  def set_kpis_config(self, kpis_config: List[KpiConfig]) -> None:
    self._kpis_config = kpis_config


class PlaceCurrentState(Projection):

  def __init__(self, id: str, kpi_groups_config: List[KpiGroupConfig] = None, created_datetime:str = None, updated_datetime:str = None) -> None:
    super().__init__(id, created_datetime, updated_datetime)
    self._kpi_groups_config: List[KpiGroupConfig] = kpi_groups_config or []

  def get_kpi_groups_config(self) -> List[KpiGroupConfig]:
    return self._kpi_groups_config

  def set_kpi_groups_config(self, kpi_groups_config: List[KpiGroupConfig]) -> None:
    self._kpi_groups_config = kpi_groups_config
    self.set_updated_datetime()


class PlaceCurrentStateService(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, place_created_dto: PlaceCreatedDto) -> PlaceCurrentState:
    raise NotImplementedError


class PlaceCurrentStateRepository(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, id: str) -> PlaceCurrentState:
    raise NotImplementedError

  @abstractmethod
  def get_all(self) -> List[PlaceCurrentState]:
    raise NotImplementedError
