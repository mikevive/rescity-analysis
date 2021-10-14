from abc import ABCMeta, abstractmethod
from typing import Tuple

from application.bounded_contexts.analysis.domain.model._entity import Entity
from application.bounded_contexts.analysis.domain.model._event import Event

from application.services.dtos.event_dto import EventDto
from application.services.dtos.kpi_create_dto import KpiCreateDto
from application.services.dtos.kpi_created_dto import KpiCreatedDto
from application.services.dtos.kpi_update_dto import KpiUpdateDto

class Kpi(Entity):

  def __init__(self, id: str = None) -> None:
    super().__init__(id)

  # Events

  class Created(Event):
    def __init__(self, kpi_id: str, name: str, equation: str, units: str) -> None:
      data: dict = {
        'name': name,
        'equation': equation,
        'units': units
      }
      super().__init__('created', kpi_id, 'kpi', data)

  class Updated(Event):
    def __init__(self, kpi_id: str, name: str, equation: str, units: str) -> None:
      data: dict = {
        'name': name,
        'equation': equation,
        'units': units
      }
      super().__init__('updated', kpi_id, 'kpi', data)

  class Delete(Event):
    def __init__(self, kpi_id: str) -> None:
      data: dict = { }
      super().__init__('deleted', kpi_id, 'kpi', data)

  class Calculated(Event):
    def __init__(self, kpi_id: str, value: float, alarms: list) -> None:

      alarms_mapped: list = []
      for alarm in alarms:
        alarms_mapped.append({
          'alarm_id:': alarm.get_alarm_id(),
          'activation:': alarm.get_activation(),
          'setpoint:': alarm.get_setpoint()
        })

      data: dict = {
        'value': value,
        'alarms': alarms_mapped
      }
      super().__init__('calculated', kpi_id, 'kpi', data)

  # Behaviours

  def update(self, name: str, equation: str, units: str) -> Event:
    event: Event = Kpi.Updated(self.get_id(), name, equation, units)
    return event

  def delete(self) -> Event:
    event: Event = Kpi.Delete(self.get_id())
    return event

  # TODO: Type constant list
  def calculate(self, equation:str, input:float, constants: list, alarms_config: list) -> Event:
    globals()['x'] = input
    for constant in constants:
      globals()[constant.get_name()] = constant.get_value()

    result: float = eval(equation)
    # TODO: Calculate Alarm
    alarms: list = []
    print(f'result:{result}')
    print(f'alarms_config found on kpi_config:{len(alarms_config)}')
    for alarm_config in alarms_config:
      print(f"{result} is {alarm_config.get_activation()} {alarm_config.get_setpoint()}")
      if(alarm_config.get_activation() == 'GREATER_THAN' and result > alarm_config.get_setpoint()):
        print("YES")
        alarms.append(alarm_config)

      elif(alarm_config.get_activation() == 'LESS_THAN' and result < alarm_config.get_setpoint()):
        print("YES")
        alarms.append(alarm_config)

      else:
        print("NO")
    # TODO: Get Setpoint
    event: Event = Kpi.Calculated(self.get_id(), result, alarms)
    return event


class KpiFactory():

  def create(name: str, equation: str, units: str) -> Tuple[Kpi, Event]:
    kpi: Kpi = Kpi()
    event: Event = Kpi.Created(kpi.get_id(), name, equation, units)
    return kpi, event

  def instantiate(id: str) -> Kpi:
    return Kpi(id)


class KpiService(metaclass=ABCMeta):

  @abstractmethod
  def create(self, kpi_create_dto: KpiCreateDto) -> KpiCreatedDto:
    raise NotImplementedError

  @abstractmethod
  def update(self, kpi_update_dto: KpiUpdateDto) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete(self, kpi_created_dto: KpiCreatedDto) -> None:
    raise NotImplementedError

  @abstractmethod
  def calculate(self, event_dto: EventDto) -> None:
    raise NotImplementedError
