from mongoengine import Document, StringField, DateTimeField, ObjectIdField, DictField
from bson import ObjectId

from application.bounded_contexts.analysis.domain.model.event import Event
from application.bounded_contexts.analysis.domain.model.kpi import Kpi, KpiRepository

class KpiMongodb(Document):
  meta = {'collection': 'kpi'}
  id = ObjectIdField(primary_key=True, required = True)
  type = StringField(max_length = 50, required = True)
  aggregate_id = ObjectIdField(required = True)
  aggregate_type = StringField(max_length = 50, required = True)
  timestamp = DateTimeField(required = True)
  data = DictField(required = True)

class KpiMongodbRepository(KpiRepository):

  def __init__(self):
    self._kpi_mongodb_mapper = KpiMongodbMapper()

  def get_by_id(self, kpi_id: ObjectId) -> Kpi:
    eventsMongodb: list[KpiMongodb] = KpiMongodb.objects(aggregate_id= kpi_id)
    kpi: Kpi = Kpi(kpi_id)
    for eventMongodb in eventsMongodb:
      event: Event = self._kpi_mongodb_mapper.to_entity(eventMongodb)
      print(event.__dict__)
      kpi.add_event(event)

    return kpi

  def save(self, kpi_event: Event) -> None:
    kpi_mongodb: KpiMongodb = self._kpi_mongodb_mapper.to_data(kpi_event)
    kpi_mongodb.save()

class KpiMongodbMapper():

  def to_entity(self, eventMongodb: KpiMongodb) -> Event:
    return Event(
      id = eventMongodb.id,
      type = eventMongodb.type,
      aggregate_id = eventMongodb.aggregate_id,
      aggregate_type = eventMongodb.aggregate_type,
      timestamp = eventMongodb.timestamp,
      data = eventMongodb.data
    )

  def to_data(self, kpi_event: Event) -> KpiMongodb:
    return KpiMongodb(
      id = kpi_event._id,
      type = kpi_event._type,
      aggregate_id = kpi_event._aggregate_id,
      aggregate_type = kpi_event._aggregate_type,
      timestamp = kpi_event._timestamp,
      data = kpi_event._data
    )
