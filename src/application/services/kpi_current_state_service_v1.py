from application.services.dtos.kpi_created_dto import KpiCreatedDto
from application.services.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateRepository, KpiCurrentStateService
from application.services.dtos.event_dto import EventDto
from infrastructure.repositories.exceptions.exceptions import KpiNotFoundError

class KpiCurrentStateServiceV1(KpiCurrentStateService):

  def __init__(self, kpi_current_state_repository: KpiCurrentStateRepository):
    self._kpi_current_state_repository: KpiCurrentStateRepository = kpi_current_state_repository


  def get_by_id(self, kpi_created_dto: KpiCreatedDto) -> KpiCurrentState:
    kpi_id: str = kpi_created_dto.get_id()
    try:
      kpi_current_state: KpiCurrentState = self._kpi_current_state_repository.get_by_id(kpi_id)
    except KpiNotFoundError as error:
      raise error

    return kpi_current_state


  def create(self, event_dto: EventDto) -> None:
    kpi_id: str = event_dto.get_aggregate_id()
    data: dict = event_dto.get_data()
    kpi_current_state: KpiCurrentState = KpiCurrentState(kpi_id, data['name'], data['equation'], data['units'])
    self._kpi_current_state_repository.save(kpi_current_state)


  def update(self, event_dto: EventDto) -> None:

    kpi_created_dto: KpiCreatedDto = KpiCreatedDto(event_dto.get_aggregate_id())

    try:
      kpi_current_state: KpiCurrentState = self.get_by_id(kpi_created_dto)
    except KpiNotFoundError as error:
      raise error

    data: dict = event_dto.get_data()

    kpi_current_state.set_name(data['name'])
    kpi_current_state.set_equation(data['equation'])
    kpi_current_state.set_units(data['units'])

    self._kpi_current_state_repository.save(kpi_current_state)


  def delete(self, event_dto: EventDto) -> None:
    kpi_id: str = event_dto.get_aggregate_id()

    kpi_created_dto: KpiCreatedDto = KpiCreatedDto(kpi_id)

    try:
      kpi_current_state: KpiCurrentState = self.get_by_id(kpi_created_dto)
    except KpiNotFoundError as error:
      raise error

    self._kpi_current_state_repository.delete(kpi_current_state)