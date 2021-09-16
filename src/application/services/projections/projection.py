from abc import ABCMeta
from bson import ObjectId

class Projection(metaclass=ABCMeta):

  def __init__(self, id: ObjectId) -> None:
    self._id: ObjectId = id

  def get_id(self) -> ObjectId:
    return self._id