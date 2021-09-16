from kafka import KafkaProducer
from application.bounded_contexts.analysis.domain.model.event import Event, EventProducer
import time

class KafkaEvent:

  def __init__(self, event: Event) -> None:
    self.id: str = str(event.get_id())
    self.type: str = event.get_type()
    self.aggregate_id: str = str(event.get_aggregate_id())
    self.aggregate_type: str = event.get_aggregate_type()
    self.data: dict = event.get_data()
    self.timestamp: int = int(time.mktime(event.get_timestamp().timetuple()))

class EventKafkaProducer(EventProducer):

  def __init__(self, kafka_producer: KafkaProducer) -> None:
      self._kafka_producer: KafkaProducer = kafka_producer

  def publish(self, topic: str, event: Event) -> None:
    print(f'>> Enviando {event.get_id()} al topico {topic}')
    kafka_event = KafkaEvent(event)
    self._kafka_producer.send(topic, kafka_event)

