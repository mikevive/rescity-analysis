from typing import List
from bson import ObjectId
from mongoengine import Document, StringField, ObjectIdField, DateTimeField, ReferenceField, ListField

from application.services.projections.kpi_current_state import KpiCurrentState
from application.services.projections.kpi_group_current_state import KpiGroupCurrentState, KpiGroupCurrentStateRepository

from infrastructure.repositories.exceptions.exceptions import KpiGroupNotFoundError
from src.infrastructure.repositories.projections.kpi_current_state_mongodb import KpiCurrentStateMongodb, KpiCurrentStateMongodbRepository

class KpiGroupCurrentStateMongodb(Document):
  meta = {'collection': 'kpi_group_current_state'}
  id = ObjectIdField(primary_key=True, required = True)
  name = StringField(max_length = 50, required = True)
  kpis = ListField(ObjectIdField(primary_key=True, required = True))
  created_datetime = DateTimeField(required=True)
  updated_datetime = DateTimeField(required=True)

class KpiGroupCurrentStateMongodbRepository(KpiGroupCurrentStateRepository):

  def get_by_id(self, id: str) -> KpiGroupCurrentState:
    try:
      kpi_group_current_state_mongodb: KpiGroupCurrentStateMongodb = KpiGroupCurrentStateMongodb.objects.get(id = ObjectId(id))
    except:
      raise KpiGroupNotFoundError

    kpi_group_current_state: KpiGroupCurrentState = self.__to_entity(kpi_group_current_state_mongodb)

    return kpi_group_current_state

  def get_all(self) -> List[KpiGroupCurrentState]:
    raise NotImplementedError


  def save(self, kpi_group_current_state: KpiGroupCurrentState) -> None:
    kpi_group_current_state_mongodb: KpiGroupCurrentStateMongodb = self.__to_data(kpi_group_current_state)
    kpi_group_current_state_mongodb.save()


  def delete(self, kpi_group_current_state: KpiGroupCurrentState) -> None:
    kpi_group_current_state_mongodb: KpiGroupCurrentStateMongodb = self.__to_data(kpi_group_current_state)
    kpi_group_current_state_mongodb.delete()


  # TODO: Inject Mappers
  def __to_entity(self, kpi_group_current_state_mongodb: KpiGroupCurrentStateMongodb) -> KpiGroupCurrentState:
#
    kpis_id: List[str] = []

    for kpi_current_state_mongodb_id in kpi_group_current_state_mongodb.kpis:
        kpis_id.append(str(kpi_current_state_mongodb_id))

    return KpiGroupCurrentState(
      id = str(kpi_group_current_state_mongodb.id),
      name = kpi_group_current_state_mongodb.name,
      kpis = kpi_group_current_state_mongodb.kpis,
      created_datetime = kpi_group_current_state_mongodb.created_datetime,
      updated_datetime = kpi_group_current_state_mongodb.updated_datetime
    )


  def __to_data(self, kpi_group_current_state: KpiGroupCurrentState) -> KpiGroupCurrentStateMongodb:

    kpis: List[ObjectId] = []

    for kpi_current_state_id in kpi_group_current_state.get_kpis():
      kpi = ObjectId(kpi_current_state_id)
      kpis.append(kpi)

    return KpiGroupCurrentStateMongodb(
      id = ObjectId(kpi_group_current_state.get_id()),
      name = kpi_group_current_state.get_name(),
      kpis = kpis,
      created_datetime = kpi_group_current_state.get_created_datetime(),
      updated_datetime = kpi_group_current_state.get_updated_datetime()
    )
