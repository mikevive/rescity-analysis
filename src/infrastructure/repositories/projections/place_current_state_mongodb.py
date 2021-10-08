from bson import ObjectId
from mongoengine import Document, EmbeddedDocument, StringField, ObjectIdField, DateTimeField, EmbeddedDocumentListField, FloatField

from application.services.projections.place_current_state import Constant, KpiConfig, KpiGroupConfig, PlaceCurrentState, PlaceCurrentStateRepository, Setpoint
from infrastructure.repositories.exceptions.exceptions import PlaceNotFoundError

class SetpointMongodb(EmbeddedDocument):
  meta = {'collection': 'place_current_state'}
  activation = StringField(required = True)
  value = FloatField(required = True)
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
  setpoints = EmbeddedDocumentListField(SetpointMongodb, default= [])


class KpiGroupConfigMongodb(EmbeddedDocument):
  meta = {'collection': 'place_current_state'}
  kpi_groud_id = ObjectIdField(primary_key=True, required = True)
  kpi_config = EmbeddedDocumentListField(KpiConfigMongodb, default= [])


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

  def get_all(self) -> list[PlaceCurrentState]:
    raise NotImplementedError


  # TODO: Inject Mappers
  def __to_entity(self, place_current_state_mongodb: PlaceCurrentStateMongodb) -> PlaceCurrentState:

    place_current_state: PlaceCurrentState = PlaceCurrentState(place_current_state_mongodb.id)

    for kpi_group_config_mongodb in place_current_state_mongodb.kpi_groups_config:
      kpi_group_config: KpiGroupConfig = KpiGroupConfig(str(kpi_group_config_mongodb.kpi_groud_id))

      for kpi_config_mongodb in kpi_group_config_mongodb.kpi_config:
        kpi_config: KpiConfig = KpiConfig(str(kpi_config_mongodb.kpi_id), str(kpi_config_mongodb.sensor_id))

        for kpi_constant_mongodb in kpi_config_mongodb.constants:
          constant: Constant = Constant(kpi_constant_mongodb.name, kpi_constant_mongodb.value)
          kpi_config.get_constants().append(constant)

        kpi_group_config.get_kpis_config().append(kpi_config)

        for kpi_setpoint_mongodb in kpi_config_mongodb.setpoints:
          setpoint: Setpoint = Setpoint(kpi_setpoint_mongodb.activation, kpi_setpoint_mongodb.value, str(kpi_setpoint_mongodb.alarm_id))
          kpi_config.get_setpoints().append(setpoint)

        kpi_group_config.get_kpis_config().append(kpi_config)

      place_current_state.get_kpi_groups_config().append(kpi_group_config)

    return place_current_state
