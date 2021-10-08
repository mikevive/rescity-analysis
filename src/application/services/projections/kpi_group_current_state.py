from abc import ABCMeta, abstractmethod

from application.services.dtos.kpi_group_created_dto import KpiGroupCreatedDto
from application.services.projections._projection import Projection
from application.services.dtos.event_dto import EventDto

class KpiGroupCurrentState(Projection):

  def __init__(self, id: str, name: str, kpis: list[str] = [], created_datetime:str = None, updated_datetime:str = None) -> None:
    super().__init__(id, created_datetime, updated_datetime)
    self._name = name
    self._kpis = kpis

  def get_name(self) -> str:
    return self._name

  def get_kpis(self) -> list[str]:
    return self._kpis

  def set_name(self, name: str) -> None:
    self._name = name
    self.set_updated_datetime()

  def set_kpis(self, kpis: list[str]) -> None:
    self._kpis = kpis
    self.set_updated_datetime()


class KpiGroupCurrentStateService(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, kpi_group_created_dto: KpiGroupCreatedDto) -> KpiGroupCurrentState:
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


class KpiGroupCurrentStateRepository(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, id: str) -> KpiGroupCurrentState:
    raise NotImplementedError

  @abstractmethod
  def get_all(self) -> list[KpiGroupCurrentState]:
    raise NotImplementedError

  @abstractmethod
  def save(self, kpi_group_created_dto: KpiGroupCurrentState) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete(self, kpi_group_created_dto: KpiGroupCurrentState) -> None:
    raise NotImplementedError