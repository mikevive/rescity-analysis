from bson.objectid import ObjectId
from application.bounded_contexts.analysis.domain.model.event import Event, EventProducer
from application.bounded_contexts.analysis.domain.model.kpi import Kpi, KpiFactory, KpiService

class KpiServiceV1(KpiService):

  def __init__(self, event_producer: EventProducer):
    self._event_producer: EventProducer = event_producer

  def create(self, name: str) -> str:
    kpi, event = KpiFactory.create(name)
    self._event_producer.publish('analysis', event)

    return str(kpi.get_id())

  def update_name(self, id: ObjectId, name:str) -> str:
    pass
    # TODO kpi_current_repository get by id
    # kpi: Kpi = self._kpi_repository.get_by_id(id)
    # event: Event = kpi.update_name(name)
    # self._kpi_repository.save(event)

  # def get_by_id(self, id:str) -> KpiCurrentState:
  #   return self._kpi_repository.get_by_id(id)
