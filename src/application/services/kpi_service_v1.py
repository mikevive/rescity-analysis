from application.bounded_contexts.analysis.domain.model._event import Event
from application.bounded_contexts.analysis.domain.model.kpi import Kpi, KpiFactory, KpiService
from application.services.dtos.event_dto import EventDto, EventDtoProducer
from application.services.dtos.kpi_create_dto import KpiCreateDto
from application.services.dtos.kpi_update_dto import KpiUpdateDto
from application.services.mappers.event_mapper import EventMapper
from application.services.dtos.kpi_created_dto import KpiCreatedDto
from application.services.mappers.kpi_created_mapper import KpiCreatedMapper
from application.services.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateService
from infrastructure.repositories.exceptions.exceptions import KpiNotFoundError

class KpiServiceV1(KpiService):

  # TODO implement DTOs

  def __init__(self, kpi_current_state_service: KpiCurrentStateService, event_producer: EventDtoProducer):
    self._kpi_current_state_service: KpiCurrentStateService = kpi_current_state_service
    self._event_dto_producer: EventDtoProducer = event_producer

  def create(self, kpi_create_dto: KpiCreateDto) -> str:
    kpi, event = KpiFactory.create(kpi_create_dto.get_name(), kpi_create_dto.get_equation(), kpi_create_dto.get_units())
    kpi_created_dto: KpiCreatedDto = KpiCreatedMapper().to_dto(kpi)
    event_dto: EventDto = EventMapper.to_dto(event)
    self._event_dto_producer.publish('kpi', event_dto)
    return kpi_created_dto

  def update(self, kpi_update_dto: KpiUpdateDto) -> None:

    kpi_created_dto: KpiCreatedDto = KpiCreatedDto(kpi_update_dto.get_id())

    try:
      self._kpi_current_state_service.get_by_id(kpi_created_dto)
    except KpiNotFoundError as error:
      raise error

    kpi_id: str = kpi_update_dto.get_id()
    kpi: Kpi = KpiFactory.instantiate(kpi_id)

    event: Event = kpi.update(kpi_update_dto.get_name(),kpi_update_dto.get_equation(), kpi_update_dto.get_units())
    event_dto: EventDto = EventMapper.to_dto(event)
    self._event_dto_producer.publish('kpi', event_dto)


  def delete(self, kpi_created_dto: KpiCreatedDto) -> None:

    try:
      self._kpi_current_state_service.get_by_id(kpi_created_dto)
    except KpiNotFoundError as error:
      raise error

    kpi_id: str = kpi_created_dto.get_id()
    kpi: Kpi = KpiFactory.instantiate(kpi_id)

    event: Event = kpi.delete()
    event_dto: EventDto = EventMapper.to_dto(event)
    self._event_dto_producer.publish('kpi', event_dto)


  def calculate(self, event_dto: EventDto) -> None:
    data: dict = event_dto.get_data()
    kpi_id = data['place']
    kpi_created_dto: KpiCreatedDto = KpiCreatedDto(kpi_id)

    try:
      kpi_current_state: KpiCurrentState = self._kpi_current_state_service.get_by_id(kpi_created_dto)
    except KpiNotFoundError as error:
      raise error

    kpi: Kpi = KpiFactory.instantiate(kpi_id)
    equation: str = kpi_current_state.get_equation()


    input: int = data['number_of_people']

    place_config: dict = {
      'A': 5
    }

    event: Event =  kpi.calculate(equation, input, place_config)
    event_dto: EventDto = EventMapper.to_dto(event)
    self._event_dto_producer.publish('kpi', event_dto)
