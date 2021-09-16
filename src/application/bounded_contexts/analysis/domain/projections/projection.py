from abc import ABCMeta
from bson import ObjectId

class Projection(metaclass=ABCMeta):

  def __init__(self, id: ObjectId = None) -> None:
    self._id: ObjectId = id if id != None else ObjectId()

  def get_id(self) -> ObjectId:
    return self._id