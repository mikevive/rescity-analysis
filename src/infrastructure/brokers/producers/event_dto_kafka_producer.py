from kafka import KafkaProducer

from application.services.dtos.event_dto import EventDto, EventDtoProducer

class EventDtoKafkaProducer(EventDtoProducer):

  def __init__(self, kafka_producer: KafkaProducer) -> None:
      self._kafka_producer: KafkaProducer = kafka_producer

  def publish(self, topic: str, event_dto: EventDto) -> None:
    print(f'>> Sending {event_dto.get_id()} to {topic} topic')
    self._kafka_producer.send(topic, event_dto)
