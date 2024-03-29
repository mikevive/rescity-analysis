from abc import ABCMeta, abstractmethod
from typing import List

from application.services.dtos.kpi_group_created_dto import KpiGroupCreatedDto
from application.services.projections._projection import Projection
from application.services.dtos.event_dto import EventDto

class KpiGroupCurrentState(Projection):

  def __init__(self, id: str, name: str, kpis: List[str] = None, created_datetime:str = None, updated_datetime:str = None) -> None:
    super().__init__(id, created_datetime, updated_datetime)
    self._name = name
    self._kpis = kpis or []

  def get_name(self) -> str:
    return self._name

  def get_kpis(self) -> List[str]:
    return self._kpis

  def set_name(self, name: str) -> None:
    self._name = name
    self.set_updated_datetime()

  def set_kpis(self, kpis: List[str]) -> None:
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
  def get_all(self) -> List[KpiGroupCurrentState]:
    raise NotImplementedError

  @abstractmethod
  def save(self, kpi_group_created_dto: KpiGroupCurrentState) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete(self, kpi_group_created_dto: KpiGroupCurrentState) -> None:
    raise NotImplementedError