from bson.objectid import ObjectId
from kafka import KafkaConsumer

from application.bounded_contexts.analysis.domain.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateService
from application.dtos.event_dto import EventDto, EventDtoFactory

class KpiCurrentStateKafkaConsumer:

  def __init__(self, kafka_consumer: KafkaConsumer, kpi_current_state_service: KpiCurrentStateService) -> None:
    self._kafka_consumer: KafkaConsumer = kafka_consumer
    self._kpi_current_state_service: KpiCurrentStateService = kpi_current_state_service

    for msg in self._kafka_consumer:
      topic: str = msg.topic
      event_dto: EventDto = EventDtoFactory.create(**msg.value)

      print(f'>> Consumiendo {event_dto.get_id()} del topico {topic}')


      aggregate_id = event_dto.get_aggregate_id()
      data = event_dto.get_data()
      self._kpi_current_state_service.create(ObjectId(aggregate_id), data['name'])