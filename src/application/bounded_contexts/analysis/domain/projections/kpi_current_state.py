from abc import ABCMeta, abstractmethod
from bson import ObjectId

from application.bounded_contexts.analysis.domain.projections.projection import Projection

class KpiCurrentState(Projection):

  def __init__(self, name: str, id: ObjectId = None) -> None:
    super().__init__(id)
    self._name = name

  def get_name(self) -> str:
    return self._name

class KpiCurrentStateService(metaclass=ABCMeta):

  @abstractmethod
  def create(self, id: ObjectId, name: str) -> None:
    raise NotImplementedError

  @abstractmethod
  def update_name(self, kpi_current_state: KpiCurrentState) -> None:
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