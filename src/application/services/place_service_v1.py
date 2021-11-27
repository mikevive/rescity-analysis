from typing import List
from injector import inject

from application.bounded_contexts.analysis.domain.model._event import Event
from application.bounded_contexts.analysis.domain.model.place import Place, PlaceFactory, PlaceService
from application.services.dtos.event_dto import EventDto, EventDtoProducer
from application.services.dtos.place_created_dto import PlaceCreatedDto
from application.services.mappers.event_mapper import EventMapper
from application.services.dtos.kpi_created_dto import KpiCreatedDto
from application.services.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateService
from application.services.projections.place_current_state import PlaceCurrentState, PlaceCurrentStateService
from infrastructure.repositories.exceptions.exceptions import KpiNotFoundError, PlaceNotFoundError

class PlaceServiceV1(PlaceService):

  @inject
  def __init__(self, kpi_current_state_service: KpiCurrentStateService, place_current_state_service: PlaceCurrentStateService, event_producer: EventDtoProducer):
    self._kpi_current_state_service: KpiCurrentStateService = kpi_current_state_service
    self._place_current_state_service: PlaceCurrentStateService = place_current_state_service
    self._event_dto_producer: EventDtoProducer = event_producer

  def calculate(self, event_dto: EventDto) -> None:
    data: dict = event_dto.get_data()
    place_id: str = data['place_id']
    sensor_id: str = event_dto.get_aggregate_id()
    measurements: List[dict] = data['measurements']

    place_created_dto: PlaceCreatedDto = PlaceCreatedDto(place_id)

    try:
      place_current_state: PlaceCurrentState = self._place_current_state_service.get_by_id(place_created_dto)
    except PlaceNotFoundError as error:
      raise error

    print(f"kpi_group_config found: {len(place_current_state.get_kpi_groups_config())}")

    place: Place = PlaceFactory.instantiate(place_id)

    print("🔥🔥🔥🔥🔥")

    for kpi_group_config in place_current_state.get_kpi_groups_config():
      print("💧 kpi group")
      for kpi_config in kpi_group_config.get_kpis_config():
        print("🍾 kpi config")
        sensorId = kpi_config.get_sensor_id()
        if kpi_config.get_sensor_id() == sensor_id:
          print(f'sensor {sensorId} found')
          for measurement in measurements:
            print(measurement)
            measurementName = measurement.get('name')
            if measurement.get('name') == kpi_config.get_measurement():
              print(f'measurement {measurementName} found')
              value_found: float = measurement.get('value')

              kpi_created_dto: KpiCreatedDto = KpiCreatedDto(kpi_config.get_kpi_id())

              try:
                kpi_current_state: KpiCurrentState = self._kpi_current_state_service.get_by_id(kpi_created_dto)
              except KpiNotFoundError as error:
                raise error

              equation: str = kpi_current_state.get_equation()

              event: Event = place.calculate(equation, value_found, kpi_config)
              event_dto: EventDto = EventMapper.to_dto(event)
              self._event_dto_producer.publish('place', event_dto)

            else:
              # TODO: If measurement not found what?
              print(f'measurement {measurementName} not found')

        else:
          # TODO: If sensor not found what?
          print(f'sensor {sensorId} not found')
