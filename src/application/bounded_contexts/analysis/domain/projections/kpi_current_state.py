from abc import ABCMeta, abstractmethod
from bson import ObjectId

from application.bounded_contexts.analysis.domain.projections.projection import Projection
from application.services._dtos.event_dto import EventDto

class KpiCurrentState(Projection):

  def __init__(self, id: ObjectId, name: str) -> None:
    super().__init__(id)
    self._name = name

  def get_name(self) -> str:
    return self._name

class KpiCurrentStateService(metaclass=ABCMeta):

  @abstractmethod
  def create(self, event_dto: EventDto) -> None:
    raise NotImplementedError

  @abstractmethod
  def update_name(self, event_dto: EventDto) -> None:
    raise NotImplementedError


class KpiCurrentStateRepository(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, id: ObjectId) -> KpiCurrentState:
    raise NotImplementedError

  @abstractmethod
  def get_all(self) -> list[KpiCurrentState]:
    raise NotImplementedError

  @abstractmethod
  def save(self, kpi: KpiCurrentState) -> None:
    raise NotImplementedError