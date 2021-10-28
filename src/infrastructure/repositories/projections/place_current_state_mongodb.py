from typing import List
from bson import ObjectId
from mongoengine import Document, EmbeddedDocument, StringField, ObjectIdField, DateTimeField, EmbeddedDocumentListField, FloatField

from application.services.projections.place_current_state import Constant, KpiConfig, KpiGroupConfig, PlaceCurrentState, PlaceCurrentStateRepository, AlarmConfig
from infrastructure.repositories.exceptions.exceptions import PlaceNotFoundError

class AlarmConfigMongodb(EmbeddedDocument):
  meta = {'collection': 'place_current_state'}
  activation = StringField(required = True)
  setpoint = FloatField(required = True)
  alarm_id = ObjectIdField(required = True)


class ConstantMongodb(EmbeddedDocument):
  meta = {'collection': 'place_current_state'}
  name = StringField(max_length = 3, required = True)
  value = FloatField(required = True)


class KpiConfigMongodb(EmbeddedDocument):
  meta = {'collection': 'place_current_state'}
  kpi_id = ObjectIdField(primary_key=True, required = True)
  sensor_id = ObjectIdField(required = True)
  constants = EmbeddedDocumentListField(ConstantMongodb, default= [])
  alarms_config = EmbeddedDocumentListField(AlarmConfigMongodb, default= [])


class KpiGroupConfigMongodb(EmbeddedDocument):
  meta = {'collection': 'place_current_state'}
  kpi_groud_id = ObjectIdField(primary_key=True, required = True)
  kpis_config = EmbeddedDocumentListField(KpiConfigMongodb, default= [])


class PlaceCurrentStateMongodb(Document):
  meta = {'collection': 'place_current_state'}
  id = ObjectIdField(primary_key=True, required = True)
  kpi_groups_config = EmbeddedDocumentListField(KpiGroupConfigMongodb, default= [])
  created_datetime = DateTimeField(required=True)
  updated_datetime = DateTimeField(required=True)


class PlaceCurrentStateMongodbRepository(PlaceCurrentStateRepository):

  def get_by_id(self, id: str) -> PlaceCurrentState:
    try:
      place_current_state_mongodb: PlaceCurrentStateMongodb = PlaceCurrentStateMongodb.objects.get(id = ObjectId(id))
    except:
      raise PlaceNotFoundError

    place_current_state: PlaceCurrentState = self.__to_entity(place_current_state_mongodb)

    return place_current_state


  def get_all(self) -> List[PlaceCurrentState]:
    raise NotImplementedError


  # TODO: Inject Mappers
  def __to_entity(self, place_current_state_mongodb: PlaceCurrentStateMongodb) -> PlaceCurrentState:

    place_current_state: PlaceCurrentState = PlaceCurrentState(place_current_state_mongodb.id)

    for kpi_group_config_mongodb in place_current_state_mongodb.kpi_groups_config:
      kpi_group_config: KpiGroupConfig = KpiGroupConfig(str(kpi_group_config_mongodb.kpi_groud_id))
      place_current_state.get_kpi_groups_config().append(kpi_group_config)

      for kpi_config_mongodb in kpi_group_config_mongodb.kpis_config:
        kpi_config: KpiConfig = KpiConfig(str(kpi_config_mongodb.kpi_id), str(kpi_config_mongodb.sensor_id))
        kpi_group_config.get_kpis_config().append(kpi_config)

        for kpi_constant_mongodb in kpi_config_mongodb.constants:
          constant: Constant = Constant(kpi_constant_mongodb.name, kpi_constant_mongodb.value)
          kpi_config.get_constants().append(constant)

        for alarm_config_mongodb in kpi_config_mongodb.alarms_config:
          alarm_config: AlarmConfig = AlarmConfig(alarm_config_mongodb.activation, alarm_config_mongodb.setpoint, str(alarm_config_mongodb.alarm_id))
          kpi_config.get_alarms_config().append(alarm_config)

    return place_current_state
