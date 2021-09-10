from datetime import datetime
from bson import ObjectId

class Event:

  def __init__(self, type: str, aggregate_id: ObjectId, aggregate_type: str, data: dict, id: ObjectId = None, timestamp: datetime = None) -> None:
    self._id: ObjectId = id if id != None else ObjectId()
    self._type: str = type
    self._aggregate_id: ObjectId = aggregate_id
    self._aggregate_type: str = aggregate_type
    self._data: dict = data
    self._timestamp: datetime = timestamp if timestamp != None else datetime.utcnow()

  def get_id(self) -> ObjectId:
    return self._id

  def get_type(self) -> str:
    return self._type

  def get_aggregate_id(self) -> ObjectId:
    return self._aggregate_id

  def get_aggregate_type(self) -> str:
    return self._aggregate_type

  def get_data(self) -> dict:
    return self._data

  def get_timestamp(self) -> datetime:
    return self._timestamp