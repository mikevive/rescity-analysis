from bson.objectid import ObjectId
from application.bounded_contexts.analysis.domain.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateRepository, KpiCurrentStateService
from application.services._dtos.event_dto import EventDto


class KpiCurrentStateServiceV1(KpiCurrentStateService):

  def __init__(self, kpi_current_state_repository: KpiCurrentStateRepository):
    self._kpi_current_state_repository: KpiCurrentStateRepository = kpi_current_state_repository

  def create(self, event_dto: EventDto) -> None:
    aggregate_id = event_dto.get_aggregate_id()
    data: str = event_dto.get_data()
    kpi_current_state: KpiCurrentState = KpiCurrentState(aggregate_id, data['name'])
    self._kpi_current_state_repository.save(kpi_current_state)

  def update_name(self, event_dto: EventDto) -> None:
    raise NotImplementedError