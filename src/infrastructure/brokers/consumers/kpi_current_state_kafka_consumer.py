from bson.objectid import ObjectId
from kafka import KafkaConsumer

from application.services.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateService
from application.services.dtos.event_dto import EventDto

class KpiCurrentStateKafkaConsumer:

  def __init__(self, kafka_consumer: KafkaConsumer, kpi_current_state_service: KpiCurrentStateService) -> None:
    self._kafka_consumer: KafkaConsumer = kafka_consumer
    self._kpi_current_state_service: KpiCurrentStateService = kpi_current_state_service

    for msg in self._kafka_consumer:
      topic: str = msg.topic
      event_dto: EventDto = EventDto(**msg.value)
      print(f'>> Consumiendo {event_dto.get_id()} del topico {topic}')

      self._kpi_current_state_service.create(event_dto)