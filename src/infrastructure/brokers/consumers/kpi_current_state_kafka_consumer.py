from kafka import KafkaConsumer

from application.services.projections.kpi_current_state import KpiCurrentStateService
from application.services.dtos.event_dto import EventDto

class KpiCurrentStateKafkaConsumer:

  def __init__(self, kafka_consumer: KafkaConsumer, kpi_current_state_service: KpiCurrentStateService) -> None:
    self._kafka_consumer: KafkaConsumer = kafka_consumer
    self._kpi_current_state_service: KpiCurrentStateService = kpi_current_state_service

    hanlders: dict = {
        'created': self._kpi_current_state_service.create,
        'updated': self._kpi_current_state_service.update,
        'deleted': self._kpi_current_state_service.delete,
      }

    for msg in self._kafka_consumer:
      topic: str = msg.topic
      event_dto: EventDto = EventDto(**msg.value)

      event_id: str = event_dto.get_id()
      event_type: str = event_dto.get_type()
      print(f'>> Consuming event {event_id} from {topic} with type {event_type}')

      try:
        hanlders[event_type](event_dto)
      except KeyError:
        print(f'>> Handler for type {event_type} not implemented yet')
