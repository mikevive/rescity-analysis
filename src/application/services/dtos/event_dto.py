from abc import ABCMeta, abstractmethod

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

class EventDtoProducer(metaclass=ABCMeta):

  @abstractmethod
  def publish(self, topic: str, event_dto: EventDto) -> None:
    raise NotImplementedError