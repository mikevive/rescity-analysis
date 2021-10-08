from abc import ABCMeta, abstractmethod

from application.services.dtos.place_created_dto import PlaceCreatedDto
from application.services.projections._projection import Projection
from application.services.dtos.event_dto import EventDto

class Setpoint:

  def __init__(self, activation: str, value: float, alarm_id: str) -> None:
    self._activation: str = activation
    self._value: int = value
    self._alarm_id: str = alarm_id

  def get_activation(self) -> str:
    return self._activation

  def set_activation(self, activation: str) -> None:
    self._activation = activation

  def get_value(self) -> float:
    return self._value

  def set_value(self, value: float) -> None:
    self._value = value

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

  def __init__(self, kpi_id: str, sensor_id: str, constants: list[Constant] = [], setpoints: list[Setpoint] = []) -> None:
    self._kpi_id: str = kpi_id
    self._sensor_id: str = sensor_id
    self._constants: list[Constant] = constants
    self._setpoints: list[Setpoint] = setpoints

  def get_kpi_id(self) -> str:
    return self._kpi_id

  def get_sensor_id(self) -> str:
    return self._sensor_id

  def get_constants(self) -> list[Constant]:
    return self._constants

  def get_setpoints(self) -> list[Constant]:
    return self._setpoints

  def set_sensor_id(self, sensor_id: str) -> None:
    self._sensor_id = sensor_id

  def set_constants(self, constants: list[Constant]) -> None:
    self._constants = constants

  def set_setpoints(self, setpoints: list[Setpoint]) -> None:
    self._setpoints = setpoints


class KpiGroupConfig:

  def __init__(self, kpi_group_id: str, kpis_config: list[KpiConfig] = []) -> None:
    self._kpi_group_id: str = kpi_group_id
    self._kpis_config: list[KpiConfig] = kpis_config

  def get_kpi_group_id(self) -> str:
    return self._kpi_group_id

  def get_kpis_config(self) -> list[KpiConfig]:
    return self._kpis_config

  def set_kpis_config(self, kpis_config: list[KpiConfig]) -> None:
    self._kpis_config = kpis_config


class PlaceCurrentState(Projection):

  def __init__(self, id: str, kpi_groups_config: list[KpiGroupConfig] = [], created_datetime:str = None, updated_datetime:str = None) -> None:
    super().__init__(id, created_datetime, updated_datetime)
    self._kpi_groups_config: list[KpiGroupConfig] = kpi_groups_config

  def get_kpi_groups_config(self) -> list[KpiGroupConfig]:
    return self._kpi_groups_config

  def set_kpi_groups_config(self, kpi_groups_config: list[KpiGroupConfig]) -> None:
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
  def get_all(self) -> list[PlaceCurrentState]:
    raise NotImplementedError
