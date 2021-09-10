from application.bounded_contexts.analysis.domain.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateRepository
from mongoengine import Document, StringField
from bson import ObjectId

class KpiCurrentStateMongodb(Document):
  meta = {'collection': 'kpi_current_state'}
  name = StringField(max_length = 50, required = True)


class KpiCurrentStateMongodbRepository(KpiCurrentStateRepository):

  def __init__(self):
    self._kpi_current_state_mongodb_mapper = KpiCurrentStateMongodbMapper()

  def get_by_id(self, id: int) -> KpiCurrentState:
    kpi_current_state_mongodb = KpiCurrentStateMongodb.objects.get(id = ObjectId(id))
    kpi_current_state = self._kpi_current_state_mongodb_mapper.to_entity(kpi_current_state_mongodb)
    return kpi_current_state

  def get_all(self):
    raise NotImplementedError

  def save(self, kpi_current_state: KpiCurrentState):
    kpi_current_state_mongodb: KpiCurrentStateMongodb = self._kpi_current_state_mongodb_mapper.to_data(kpi_current_state)
    kpi_current_state_mongodb.save()

class KpiCurrentStateMongodbMapper():

  def to_entity(self, kpi_current_state_mongodb: KpiCurrentStateMongodb) -> KpiCurrentState:
    return KpiCurrentState(name = kpi_current_state_mongodb.name)

  def to_data(self, kpi_current_state: KpiCurrentState) -> KpiCurrentStateMongodb:
    return KpiCurrentStateMongodb(name = kpi_current_state.name)
