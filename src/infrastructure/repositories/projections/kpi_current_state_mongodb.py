from typing import List
from application.services.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateRepository
from mongoengine import Document, StringField, ObjectIdField, DateTimeField
from bson import ObjectId

from infrastructure.repositories.exceptions.exceptions import KpiNotFoundError

class KpiCurrentStateMongodb(Document):
  meta = {'collection': 'kpi_current_state'}
  id = ObjectIdField(primary_key=True, required = True)
  name = StringField(max_length = 50, required = True)
  equation = StringField(max_length = 100, required = True)
  units = StringField(max_length = 20, required = True)
  created_datetime = DateTimeField(required=True)
  updated_datetime = DateTimeField(required=True)

class KpiCurrentStateMongodbRepository(KpiCurrentStateRepository):

  def get_by_id(self, id: str) -> KpiCurrentState:
    try:
      kpi_current_state_mongodb: KpiCurrentStateMongodb = KpiCurrentStateMongodb.objects.get(id = ObjectId(id))
    except:
      raise KpiNotFoundError

    kpi_current_state: KpiCurrentState = self.__to_entity(kpi_current_state_mongodb)

    return kpi_current_state

  def get_all(self) -> List[KpiCurrentState]:
    raise NotImplementedError


  def save(self, kpi_current_state: KpiCurrentState) -> None:
    kpi_current_state_mongodb: KpiCurrentStateMongodb = self.__to_data(kpi_current_state)
    kpi_current_state_mongodb.save()


  def delete(self, kpi_current_state: KpiCurrentState) -> None:
    kpi_current_state_mongodb: KpiCurrentStateMongodb = self.__to_data(kpi_current_state)
    kpi_current_state_mongodb.delete()


  # TODO: Inject Mappers
  def __to_entity(self, kpi_current_state_mongodb: KpiCurrentStateMongodb) -> KpiCurrentState:
    return KpiCurrentState(
      id = str(kpi_current_state_mongodb.id),
      name = kpi_current_state_mongodb.name,
      equation = kpi_current_state_mongodb.equation,
      units = kpi_current_state_mongodb.units,
      created_datetime = kpi_current_state_mongodb.created_datetime,
      updated_datetime = kpi_current_state_mongodb.updated_datetime
    )


  def __to_data(self, kpi_current_state: KpiCurrentState) -> KpiCurrentStateMongodb:
    return KpiCurrentStateMongodb(
      id = ObjectId(kpi_current_state.get_id()),
      name = kpi_current_state.get_name(),
      equation = kpi_current_state.get_equation(),
      units = kpi_current_state.get_units(),
      created_datetime = kpi_current_state.get_created_datetime(),
      updated_datetime = kpi_current_state.get_updated_datetime()
    )
