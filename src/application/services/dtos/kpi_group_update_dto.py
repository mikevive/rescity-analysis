from bson.objectid import ObjectId, InvalidId

from application.services.dtos.exceptions.exceptions import InvalidIdError, LongitudeNameError

class KpiGroupUpdateDto():

  def __init__(self, id: str, name: str, kpis: list[str]) -> None:
    try:
      ObjectId(id)
    except InvalidId:
      raise InvalidIdError

    self.id = id

    if(len(name) <= 50):
      self.name = name
    else:
      raise LongitudeNameError

    for kpi in kpis:
      try:
        ObjectId(kpi)
      except InvalidId:
        raise InvalidIdError

    self.kpis = kpis

  def get_id(self) -> str:
    return self.id

  def get_name(self) -> str:
    return self.name

  def get_kpis(self) -> list[str]:
    return self.kpis
