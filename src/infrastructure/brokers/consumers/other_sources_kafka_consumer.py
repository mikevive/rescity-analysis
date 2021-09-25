from kafka import KafkaConsumer

from application.bounded_contexts.analysis.domain.model.kpi import KpiService
from application.services.dtos.event_dto import EventDto

class OtherSourcesKafkaConsumer:

  def __init__(self, kafka_consumer: KafkaConsumer, kpi_service: KpiService) -> None:
    self._kafka_consumer: KafkaConsumer = kafka_consumer
    self._kpi_service: KpiService = kpi_service

    hanlders: dict = {
        'created': self._kpi_service.calculate
      }

    for msg in self._kafka_consumer:
      topic: str = msg.topic
      event_dto: EventDto = EventDto(**msg.value)

      event_id: str = event_dto.get_id()
      event_type: str = event_dto.get_type()
      print(f'>> Consuming event {event_id} from {topic} with type {event_type}')

      hanlders[event_type](event_dto)
