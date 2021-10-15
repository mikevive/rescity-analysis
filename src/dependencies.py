from injector import singleton

# Ports
from application.services.projections.kpi_current_state import KpiCurrentStateRepository, KpiCurrentStateService
from application.services.projections.kpi_group_current_state import KpiGroupCurrentStateRepository, KpiGroupCurrentStateService
from application.services.projections.place_current_state import PlaceCurrentStateRepository, PlaceCurrentStateService
from application.bounded_contexts.analysis.domain.model.kpi import KpiService
from application.bounded_contexts.analysis.domain.model.kpi_group import KpiGroupService
from application.bounded_contexts.analysis.domain.model.place import PlaceService
from application.services.dtos.event_dto import EventDtoProducer

# Adapters
from infrastructure.repositories.projections.kpi_current_state_mongodb import KpiCurrentStateMongodbRepository
from application.services.kpi_current_state_service_v1 import KpiCurrentStateServiceV1
from application.services.kpi_service_v1 import KpiServiceV1

from infrastructure.repositories.projections.kpi_group_current_state_mongodb import KpiGroupCurrentStateMongodbRepository
from application.services.kpi_group_current_state_service_v1 import KpiGroupCurrentStateServiceV1
from application.services.kpi_group_service_v1 import KpiGroupServiceV1

from infrastructure.repositories.projections.place_current_state_mongodb import PlaceCurrentStateMongodbRepository
from application.services.place_current_state_service_v1 import PlaceCurrentStateServiceV1
from application.services.place_service_v1 import PlaceServiceV1

from infrastructure.brokers.producers.event_dto_kafka_producer import EventDtoKafkaProducer

def configure(binder):
    binder.bind(KpiCurrentStateRepository, to=KpiCurrentStateMongodbRepository, scope=singleton)
    binder.bind(KpiCurrentStateService, to=KpiCurrentStateServiceV1, scope=singleton)
    binder.bind(KpiService, to=KpiServiceV1, scope=singleton)

    binder.bind(KpiGroupCurrentStateRepository, to=KpiGroupCurrentStateMongodbRepository, scope=singleton)
    binder.bind(KpiGroupCurrentStateService, to=KpiGroupCurrentStateServiceV1, scope=singleton)
    binder.bind(KpiGroupService, to=KpiGroupServiceV1, scope=singleton)

    binder.bind(PlaceCurrentStateRepository, to=PlaceCurrentStateMongodbRepository, scope=singleton)
    binder.bind(PlaceCurrentStateService, to=PlaceCurrentStateServiceV1, scope=singleton)
    binder.bind(PlaceService, to=PlaceServiceV1, scope=singleton)

    binder.bind(EventDtoProducer, to=EventDtoKafkaProducer, scope=singleton)