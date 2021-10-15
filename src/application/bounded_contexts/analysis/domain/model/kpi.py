from abc import ABCMeta, abstractmethod
from typing import Tuple

from application.bounded_contexts.analysis.domain.model._entity import Entity
from application.bounded_contexts.analysis.domain.model._event import Event

from application.services.dtos.kpi_create_dto import KpiCreateDto
from application.services.dtos.kpi_created_dto import KpiCreatedDto
from application.services.dtos.kpi_update_dto import KpiUpdateDto

class Kpi(Entity):

  def __init__(self, id: str = None) -> None:
    super().__init__(id)

  # Events

  class Created(Event):
    def __init__(self, kpi_id: str, name: str, equation: str, units: str) -> None:
      data: dict = {
        'name': name,
        'equation': equation,
        'units': units
      }
      super().__init__('created', kpi_id, 'kpi', data)

  class Updated(Event):
    def __init__(self, kpi_id: str, name: str, equation: str, units: str) -> None:
      data: dict = {
        'name': name,
        'equation': equation,
        'units': units
      }
      super().__init__('updated', kpi_id, 'kpi', data)

  class Deleted(Event):
    def __init__(self, kpi_id: str) -> None:
      data: dict = { }
      super().__init__('deleted', kpi_id, 'kpi', data)


  # Behaviours

  def update(self, name: str, equation: str, units: str) -> Event:
    event: Event = Kpi.Updated(self.get_id(), name, equation, units)
    return event

  def delete(self) -> Event:
    event: Event = Kpi.Deleted(self.get_id())
    return event


class KpiFactory:

  def create(name: str, equation: str, units: str) -> Tuple[Kpi, Event]:
    kpi: Kpi = Kpi()
    event: Event = Kpi.Created(kpi.get_id(), name, equation, units)
    return kpi, event

  def instantiate(id: str) -> Kpi:
    return Kpi(id)


class KpiService(metaclass=ABCMeta):

  @abstractmethod
  def create(self, kpi_create_dto: KpiCreateDto) -> KpiCreatedDto:
    raise NotImplementedError

  @abstractmethod
  def update(self, kpi_update_dto: KpiUpdateDto) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete(self, kpi_created_dto: KpiCreatedDto) -> None:
    raise NotImplementedError
