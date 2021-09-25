from abc import ABCMeta, abstractmethod

from application.services.dtos.kpi_created_dto import KpiCreatedDto
from application.services.projections._projection import Projection
from application.services.dtos.event_dto import EventDto

class KpiCurrentState(Projection):

  def __init__(self, id: str, name: str, equation: str, units: str, created_datetime:str = None, updated_datetime:str = None) -> None:
    super().__init__(id, created_datetime, updated_datetime)
    self._name = name
    self._equation = equation
    self._units = units

  def get_name(self) -> str:
    return self._name

  def get_equation(self) -> str:
    return self._equation

  def get_units(self) -> str:
    return self._units

  def set_name(self, name: str) -> None:
    self._name = name
    self.set_updated_datetime()

  def set_equation(self, equation: str) -> None:
    self._equation = equation
    self.set_updated_datetime()

  def set_units(self, units: str) -> None:
    self._units = units
    self.set_updated_datetime()


class KpiCurrentStateService(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, kpi_created_dto: KpiCreatedDto) -> KpiCurrentState:
    raise NotImplementedError

  @abstractmethod
  def create(self, event_dto: EventDto) -> None:
    raise NotImplementedError

  @abstractmethod
  def update(self, event_dto: EventDto) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete(self, event_dto: EventDto) -> None:
    raise NotImplementedError


class KpiCurrentStateRepository(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, id: str) -> KpiCurrentState:
    raise NotImplementedError

  @abstractmethod
  def get_all(self) -> list[KpiCurrentState]:
    raise NotImplementedError

  @abstractmethod
  def save(self, kpi_current_state: KpiCurrentState) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete(self, kpi_current_state: KpiCurrentState) -> None:
    raise NotImplementedError