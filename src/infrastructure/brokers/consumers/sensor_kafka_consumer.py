import os
from injector import inject
from kafka import KafkaConsumer
from bson import json_util
from threading import Thread
from application.bounded_contexts.analysis.domain.model.place import PlaceService
from application.services.dtos.event_dto import EventDto

class SensorKafkaConsumer:

  @inject
  def __init__(self, place_service: PlaceService) -> None:

    # Set Handlers
    self._hanlders: dict = {
      'calculated': place_service.calculate
    }

    # Kafka Consumer Config
    while True:
      try:

        self._kafka_consumer: KafkaConsumer = KafkaConsumer(
          'sensor',
          bootstrap_servers = [os.environ.get('KAFKA_HOST')+':'+os.environ.get('KAFKA_PORT')],
          auto_offset_reset = 'earliest',
          group_id = 'sensor_kafka_consumer',
          value_deserializer = lambda data: json_util.loads(data),
          reconnect_backoff_ms = 50,
          reconnect_backoff_max_ms = 1000
        )

        # Start Kafka Consumers as Threads
        Thread(
          target = self.__start_tread,
          daemon = True
        ).start()

      except Exception:
        print("Unable to connect to Kafka Broker: " + os.environ.get('KAFKA_HOST')+':'+os.environ.get('KAFKA_PORT'))
        continue

      break

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
