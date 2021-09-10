from abc import ABCMeta, abstractmethod
from typing import Tuple
from bson.objectid import ObjectId

from application.bounded_contexts.analysis.domain.model.entity import Entity
from application.bounded_contexts.analysis.domain.model.event import Event

class Kpi(Entity):

  def __init__(self, id: ObjectId = None, events: list[Event] = None) -> None:
    super().__init__(id, events)

  def update_name(self, name:str) -> Event:
    event: Event = KpiEvent.NameUpdated(self.get_id(), name)
    self.add_event(event)
    return event


class KpiFactory():

  def create(name:str) -> Tuple[Kpi, Event]:
    kpi: Kpi = Kpi()
    event: Event = KpiEvent.Created(kpi.get_id(), name)
    kpi.add_event(event)
    return kpi, event


class KpiEvent:

  class Created(Event):
    def __init__(self, kpi_id: ObjectId, name: str) -> None:
      data: dict = {'name': name}
      super().__init__('created', kpi_id, 'kpi', data)

  class NameUpdated(Event):
    def __init__(self, kpi_id: ObjectId, name: str) -> None:
      data: dict = {'name': name}
      super().__init__('name_updated', kpi_id, 'kpi', data)


class KpiRepository(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, kpi_id: ObjectId) -> Kpi:
    raise NotImplementedError

  @abstractmethod
  def save(self, kpi_event: Event) -> None:
    raise NotImplementedError