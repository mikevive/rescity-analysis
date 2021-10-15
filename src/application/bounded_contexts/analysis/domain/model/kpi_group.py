from abc import ABCMeta, abstractmethod
from typing import Tuple

from application.bounded_contexts.analysis.domain.model._entity import Entity
from application.bounded_contexts.analysis.domain.model._event import Event

from application.services.dtos.kpi_group_create_dto import KpiGroupCreateDto
from application.services.dtos.kpi_group_created_dto import KpiGroupCreatedDto
from application.services.dtos.kpi_group_update_dto import KpiGroupUpdateDto
from application.bounded_contexts.analysis.domain.model.kpi import Kpi

class KpiGroup(Entity):

  def __init__(self, id: str = None) -> None:
    super().__init__(id)

  # Events

  # TODO: use list[Kpi]
  class Created(Event):
    def __init__(self, kpi_group_id: str, name: str, kpis: list[str]) -> None:

      data: dict = {
        'name': name,
        'kpis': kpis
      }
      super().__init__('created', kpi_group_id, 'kpi_group', data)

  class Updated(Event):
    def __init__(self, kpi_group_id: str, name: str, kpis:list[str]) -> None:

      data: dict = {
        'name': name,
        'kpis': kpis
      }
      super().__init__('updated', kpi_group_id, 'kpi_group', data)

  class Deleted(Event):
    def __init__(self, kpi_group_id: str) -> None:
      data: dict = { }
      super().__init__('deleted', kpi_group_id, 'kpi_group', data)

  # Behaviours

  def update(self, name: str, kpis: list[str]) -> Event:
    event: Event = KpiGroup.Updated(self.get_id(), name, kpis)
    return event

  def delete(self) -> Event:
    event: Event = KpiGroup.Deleted(self.get_id())
    return event


class KpiGroupFactory:

  def create(name: str, kpis: list[str]) -> Tuple[KpiGroup, Event]:
    kpi_group: KpiGroup = KpiGroup()
    event: Event = KpiGroup.Created(kpi_group.get_id(), name, kpis)
    return kpi_group, event

  def instantiate(id: str) -> KpiGroup:
    return KpiGroup(id)


class KpiGroupService(metaclass=ABCMeta):

  @abstractmethod
  def create(self, kpi_create_dto: KpiGroupCreateDto) -> str:
    raise NotImplementedError

  @abstractmethod
  def update(self, kpi_update_dto: KpiGroupUpdateDto) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete(self, kpi_created_dto: KpiGroupCreatedDto) -> None:
    raise NotImplementedError
