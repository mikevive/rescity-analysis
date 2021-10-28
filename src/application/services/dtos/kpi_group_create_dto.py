from bson import ObjectId
from bson.errors import InvalidId
from application.services.dtos.exceptions.exceptions import LongitudeNameError
from src.application.services.dtos.exceptions.exceptions import InvalidIdError

class KpiGroupCreateDto():

  def __init__(self, name: str, kpis: List[str]) -> None:

    #TODO: Centralize DTO validations
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

  def get_name(self) -> str:
    return self.name

  def get_kpis(self) -> List[str]:
    return self.kpis
