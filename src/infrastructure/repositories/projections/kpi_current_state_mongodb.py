from application.services.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateRepository
from mongoengine import Document, StringField, ObjectIdField
from bson import ObjectId

class KpiCurrentStateMongodb(Document):
  meta = {'collection': 'kpi_current_state'}
  id = ObjectIdField(primary_key=True, required = True)
  name = StringField(max_length = 50, required = True)


class KpiCurrentStateMongodbRepository(KpiCurrentStateRepository):

  def get_by_id(self, id: ObjectId) -> KpiCurrentState:
    kpi_current_state_mongodb = KpiCurrentStateMongodb.objects.get(id = id)
    kpi_current_state = self.__to_entity(kpi_current_state_mongodb)
    return kpi_current_state

  def get_all(self) -> list[KpiCurrentState]:
    raise NotImplementedError

  def save(self, kpi_current_state: KpiCurrentState) -> None:
    kpi_current_state_mongodb: KpiCurrentStateMongodb = self.__to_data(kpi_current_state)
    kpi_current_state_mongodb.save()

  def __to_entity(self, kpi_current_state_mongodb: KpiCurrentStateMongodb) -> KpiCurrentState:
    return KpiCurrentState(
      id = kpi_current_state_mongodb.id,
      name = kpi_current_state_mongodb.name
    )

  def __to_data(self, kpi_current_state: KpiCurrentState) -> KpiCurrentStateMongodb:
    return KpiCurrentStateMongodb(
      id = kpi_current_state.get_id(),
      name = kpi_current_state.get_name()
    )
