from injector import inject

from application.services.dtos.place_created_dto import PlaceCreatedDto, PlaceCreatedDto
from application.services.projections.place_current_state import PlaceCurrentState
from application.services.projections.place_current_state import PlaceCurrentState, PlaceCurrentStateRepository, PlaceCurrentStateService
from infrastructure.repositories.exceptions.exceptions import PlaceNotFoundError, PlaceNotFoundError

class PlaceCurrentStateServiceV1(PlaceCurrentStateService):

  @inject
  def __init__(self, place_current_state_repository: PlaceCurrentStateRepository):
    self._place_current_state_repository: PlaceCurrentStateRepository = place_current_state_repository


  def get_by_id(self, place_created_dto: PlaceCreatedDto) -> PlaceCurrentState:
    place_id: str = place_created_dto.get_id()
    try:
      place_current_state: PlaceCurrentState = self._place_current_state_repository.get_by_id(place_id)
    except PlaceNotFoundError as error:
      raise error

    return place_current_state
