from typing import List
from injector import inject

from application.bounded_contexts.analysis.domain.model._event import Event
from application.bounded_contexts.analysis.domain.model.kpi_group import KpiGroup, KpiGroupFactory, KpiGroupService
from application.services.dtos.event_dto import EventDto, EventDtoProducer
from application.services.dtos.kpi_group_create_dto import KpiGroupCreateDto
from application.services.dtos.kpi_group_update_dto import KpiGroupUpdateDto
from application.services.mappers.event_mapper import EventMapper
from application.services.dtos.kpi_group_created_dto import KpiGroupCreatedDto
from application.services.mappers.kpi_group_created_mapper import KpiGroupCreatedMapper
from application.services.projections.kpi_current_state import KpiCurrentStateService
from application.services.projections.kpi_group_current_state import KpiGroupCurrentStateService
from infrastructure.repositories.exceptions.exceptions import KpiGroupNotFoundError, KpiNotFoundError

class KpiGroupServiceV1(KpiGroupService):

  @inject
  def __init__(self, kpi_group_current_state_service: KpiGroupCurrentStateService, kpi_current_state_service: KpiCurrentStateService, event_producer: EventDtoProducer):
    self._kpi_group_current_state_service: KpiGroupCurrentStateService = kpi_group_current_state_service
    self._kpi_current_state_service: KpiCurrentStateService = kpi_current_state_service
    self._event_dto_producer: EventDtoProducer = event_producer

  def create(self, kpi_group_create_dto: KpiGroupCreateDto) -> str:
    # TODO: VALIDATE KPI GROUP NAME DOESN'T EXIST

    errors: List[Exception] = []
    for kpi in kpi_group_create_dto.get_kpis():
      print(kpi)
      kpi_created_dto: KpiGroupCreatedDto = KpiGroupCreatedDto(kpi)

      try:
        print(kpi_created_dto.get_id())
        self._kpi_current_state_service.get_by_id(kpi_created_dto)
      except KpiNotFoundError as error:
        errors.append(error)

    if len(errors) > 0:
      raise KpiNotFoundError

    kpi_group, event = KpiGroupFactory.create(kpi_group_create_dto.get_name(), kpi_group_create_dto.get_kpis())
    kpi_group_created_dto: KpiGroupCreatedDto = KpiGroupCreatedMapper().to_dto(kpi_group)
    event_dto: EventDto = EventMapper.to_dto(event)
    self._event_dto_producer.publish('kpi_group', event_dto)
    return kpi_group_created_dto

  def update(self, kpi_group_update_dto: KpiGroupUpdateDto) -> None:

    kpi_group_created_dto: KpiGroupCreatedDto = KpiGroupCreatedDto(kpi_group_update_dto.get_id())

    try:
      self._kpi_group_current_state_service.get_by_id(kpi_group_created_dto)
    except KpiGroupNotFoundError as error:
      raise error

    errors: List[Exception] = []
    for kpi in kpi_group_update_dto.get_kpis():
      print(kpi)
      kpi_created_dto: KpiGroupCreatedDto = KpiGroupCreatedDto(kpi)

      try:
        print(kpi_created_dto.get_id())
        self._kpi_current_state_service.get_by_id(kpi_created_dto)
      except KpiNotFoundError as error:
        errors.append(error)

    if len(errors) > 0:
      raise KpiNotFoundError

    kpi_group_id: str = kpi_group_update_dto.get_id()
    kpi_group: KpiGroup = KpiGroupFactory.instantiate(kpi_group_id)

    event: Event = kpi_group.update(kpi_group_update_dto.get_name(),kpi_group_update_dto.get_kpis())
    event_dto: EventDto = EventMapper.to_dto(event)
    self._event_dto_producer.publish('kpi_group', event_dto)


  def delete(self, kpi_group_created_dto: KpiGroupCreatedDto) -> None:

    try:
      self._kpi_group_current_state_service.get_by_id(kpi_group_created_dto)
    except KpiGroupNotFoundError as error:
      raise error

    kpi_group_id: str = kpi_group_created_dto.get_id()
    kpi_group: KpiGroup = KpiGroupFactory.instantiate(kpi_group_id)

    event: Event = kpi_group.delete()
    event_dto: EventDto = EventMapper.to_dto(event)
    self._event_dto_producer.publish('kpi_group', event_dto)
