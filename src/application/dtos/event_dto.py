from abc import ABCMeta, abstractmethod
import time

from application.bounded_contexts.analysis.domain.model.event import Event

class EventDto:

  def __init__(
    self,
    id: str,
    type: str,
    aggregate_id: str,
    aggregate_type: str,
    data: dict,
    timestamp: int,
  ) -> None:
    self.id: str = id
    self.type: str = type
    self.aggregate_id: str = aggregate_id
    self.aggregate_type: str = aggregate_type
    self.data: dict = data
    self.timestamp: int = timestamp

  def get_id(self) -> str:
    return self.id

  def get_type(self) -> str:
    return self.type

  def get_aggregate_id(self) -> str:
    return self.aggregate_id

  def get_aggregate_type(self) -> str:
    return self.aggregate_type

  def get_data(self) -> dict:
    return self.data

  def get_timestamp(self) -> int:
    return self.timestamp

class EventDtoFactory():

  def create(
    id: str,
    type: str,
    aggregate_id: str,
    aggregate_type: str,
    data: dict,
    timestamp: int,
  ) -> EventDto:
    return EventDto(
      id,
      type,
      aggregate_id,
      aggregate_type,
      data,
      timestamp
    )

  def create_with_event(event: Event) -> EventDto:
    return EventDto(
      str(event.get_id()),
      event.get_type(),
      str(event.get_aggregate_id()),
      event.get_aggregate_type(),
      event.get_data(),
      int(time.mktime(event.get_timestamp().timetuple()))
    )


class EventDtoProducer(metaclass=ABCMeta):

  @abstractmethod
  def publish(self, topic: str, event_dto: EventDto) -> None:
    raise NotImplementedError