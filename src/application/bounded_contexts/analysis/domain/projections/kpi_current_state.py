from abc import ABCMeta, abstractmethod

class KpiCurrentState():

  def __init__(self, name):
    self.name = name

# class KpiCurrentStateService():


class KpiCurrentStateRepository(metaclass=ABCMeta):

  @abstractmethod
  def get_by_id(self, id) -> KpiCurrentState:
    raise NotImplementedError

  @abstractmethod
  def get_all(self) -> list[KpiCurrentState]:
    raise NotImplementedError

  @abstractmethod
  def save(self, kpi) -> None:
    raise NotImplementedError