import os
from injector import inject
from kafka import KafkaConsumer
from bson import json_util
from threading import Thread

from application.services.projections.kpi_group_current_state import KpiGroupCurrentStateService
from application.services.dtos.event_dto import EventDto

class KpiGroupCurrentStateKafkaConsumer:

  @inject
  def __init__(self, kpi_group_current_state_service: KpiGroupCurrentStateService) -> None:

    # Set Handlers
    self._hanlders: dict = {
      'created': kpi_group_current_state_service.create,
      'updated': kpi_group_current_state_service.update,
      'deleted': kpi_group_current_state_service.delete,
    }

    # Kafka Consumer Config

    try:

      self._kafka_consumer: KafkaConsumer = KafkaConsumer(
        'kpi_group',
        bootstrap_servers = [os.environ.get('KAFKA_HOST')+':'+os.environ.get('KAFKA_PORT')],
        auto_offset_reset = 'earliest',
        group_id = 'kpi_group_current_state_kafka_consumer',
        value_deserializer = lambda data: json_util.loads(data)
      )

      # Start Kafka Consumers as Threads
      Thread(
        target = self.__start_tread,
        daemon = True
      ).start()

    except Exception:
      print("Unable to connect to Kafka Broker: " + os.environ.get('KAFKA_HOST')+':'+os.environ.get('KAFKA_PORT'))


  def __start_tread(self):
    for msg in self._kafka_consumer:
      topic: str = msg.topic
      event_dto: EventDto = EventDto(**msg.value)

      event_id: str = event_dto.get_id()
      event_type: str = event_dto.get_type()
      print(f'>> Consuming event {event_id} from {topic} with type {event_type}')

      try:
        self._hanlders[event_type](event_dto)
      except KeyError:
        pass
