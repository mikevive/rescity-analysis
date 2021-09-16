from bson.objectid import ObjectId
from application.bounded_contexts.analysis.domain.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateRepository, KpiCurrentStateService


class KpiCurrentStateServiceV1(KpiCurrentStateService):

  def __init__(self, kpi_current_state_repository: KpiCurrentStateRepository):
    self._kpi_current_state_repository: KpiCurrentStateRepository = kpi_current_state_repository

  def create(self, id: ObjectId, name: str) -> None:
    kpi_current_state: KpiCurrentState = KpiCurrentState(name, id=id)
    print(f'id on create service: {str(kpi_current_state.get_id())}')
    self._kpi_current_state_repository.save(kpi_current_state)

  def update_name(self, kpi_current_state: KpiCurrentState) -> None:
    raise NotImplementedError