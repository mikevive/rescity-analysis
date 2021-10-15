from abc import ABCMeta, abstractmethod

from application.bounded_contexts.analysis.domain.model._entity import Entity
from application.bounded_contexts.analysis.domain.model._event import Event

from application.services.dtos.event_dto import EventDto
from application.services.projections.place_current_state import KpiConfig

class Place(Entity):

  def __init__(self, id: str = None) -> None:
    super().__init__(id)

  # Events

  class Calculated(Event):
    def __init__(self, place_id: str, kpi_id: str, result: float, alarms: list) -> None:

      alarms_mapped: list = []
      for alarm in alarms:
        alarms_mapped.append({
          'alarm_id:': alarm.get_alarm_id(),
          'activation:': alarm.get_activation(),
          'setpoint:': alarm.get_setpoint()
        })

      data: dict = {
        'kpi_id': kpi_id,
        'result': result,
        'alarms': alarms_mapped
      }
      super().__init__('calculated', place_id, 'place', data)

  # Behaviours

  # TODO: Type constant list
  def calculate(self, equation:str, input:float, kpi_config: KpiConfig) -> Event:
    globals()['x'] = input
    for constant in kpi_config.get_constants():
      globals()[constant.get_name()] = constant.get_value()

    result: float = eval(equation)
    # TODO: Calculate Alarm
    alarms: list = []
    print(f'result:{result}')
    print(f'alarms_config found on kpi_config:{len(kpi_config.get_alarms_config())}')
    for alarm_config in kpi_config.get_alarms_config():
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
    event: Event = Place.Calculated(self.get_id(), kpi_config.get_kpi_id(), result, alarms)
    return event


class PlaceFactory:

  def instantiate(id: str) -> Place:
    return Place(id)


class PlaceService(metaclass=ABCMeta):

  @abstractmethod
  def calculate(self, event_dto: EventDto) -> None:
    raise NotImplementedError
