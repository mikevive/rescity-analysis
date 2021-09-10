from abc import ABCMeta
from bson import ObjectId

from application.bounded_contexts.analysis.domain.model.event import Event

class Entity(metaclass=ABCMeta):

  def __init__(self, id: ObjectId = None, events: list[Event] = None) -> None:
    self._id: ObjectId = id if id != None else ObjectId()
    self._events: list[Event] = events if events != None else []

  def get_id(self) -> ObjectId:
    return self._id

  def add_event(self, event) -> None:
    self._events.append(event)