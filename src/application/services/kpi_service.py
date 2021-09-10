from bson.objectid import ObjectId
from application.bounded_contexts.analysis.domain.model.event import Event
from application.bounded_contexts.analysis.domain.model.kpi import Kpi, KpiRepository, KpiFactory

class KpiService:

  def __init__(self, kpi_event_repository: KpiRepository):
    self._kpi_repository: KpiRepository = kpi_event_repository

  def create(self, name:str) -> str:
    kpi, event = KpiFactory.create(name)
    self._kpi_repository.save(event)
    return str(kpi.get_id())

  def update_name(self, id: ObjectId, name:str) -> str:
    kpi: Kpi = self._kpi_repository.get_by_id(id)
    event: Event = kpi.update_name(name)
    self._kpi_repository.save(event)

  # def get_by_id(self, id:str) -> KpiCurrentState:
  #   return self._kpi_repository.get_by_id(id)
