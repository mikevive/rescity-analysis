from injector import inject

from application.services.dtos.kpi_group_created_dto import KpiGroupCreatedDto
from application.services.projections.kpi_group_current_state import KpiGroupCurrentState, KpiGroupCurrentStateRepository, KpiGroupCurrentStateService
from application.services.dtos.event_dto import EventDto
from infrastructure.repositories.exceptions.exceptions import KpiGroupNotFoundError

class KpiGroupCurrentStateServiceV1(KpiGroupCurrentStateService):

  @inject
  def __init__(self, kpi_group_current_state_repository: KpiGroupCurrentStateRepository):
    self._kpi_group_current_state_repository: KpiGroupCurrentStateRepository = kpi_group_current_state_repository


  def get_by_id(self, kpi_group_created_dto: KpiGroupCreatedDto) -> KpiGroupCurrentState:
    kpi_group_id: str = kpi_group_created_dto.get_id()
    try:
      kpi_group_current_state: KpiGroupCurrentState = self._kpi_group_current_state_repository.get_by_id(kpi_group_id)
    except KpiGroupNotFoundError as error:
      raise error

    return kpi_group_current_state


  def create(self, event_dto: EventDto) -> None:
    print('Service Creating')
    kpi_group_id: str = event_dto.get_aggregate_id()
    data: dict = event_dto.get_data()
    kpi_group_current_state: KpiGroupCurrentState = KpiGroupCurrentState(kpi_group_id, data['name'], data['kpis'])
    print(kpi_group_current_state.__dict__)
    self._kpi_group_current_state_repository.save(kpi_group_current_state)


  def update(self, event_dto: EventDto) -> None:

    kpi_group_created_dto: KpiGroupCreatedDto = KpiGroupCreatedDto(event_dto.get_aggregate_id())

    try:
      kpi_group_current_state: KpiGroupCurrentState = self.get_by_id(kpi_group_created_dto)
    except KpiGroupNotFoundError as error:
      raise error

    data: dict = event_dto.get_data()

    kpi_group_current_state.set_name(data['name'])
    kpi_group_current_state.set_kpis(data['kpis'])

    self._kpi_group_current_state_repository.save(kpi_group_current_state)


  def delete(self, event_dto: EventDto) -> None:
    kpi_group_id: str = event_dto.get_aggregate_id()

    kpi_group_created_dto: KpiGroupCreatedDto = KpiGroupCreatedDto(kpi_group_id)

    try:
      kpi_group_current_state: KpiGroupCurrentState = self.get_by_id(kpi_group_created_dto)
    except KpiGroupNotFoundError as error:
      raise error

    self._kpi_group_current_state_repository.delete(kpi_group_current_state)