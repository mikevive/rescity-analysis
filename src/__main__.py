from flask import Flask
from mongoengine import connect

# Ports
from application.bounded_contexts.analysis.domain.projections.kpi_current_state import KpiCurrentStateRepository

# Adapters
from infrastructure.repositories.event_store.kpi_mongodb import KpiMongodbRepository
from application.services.kpi_service import KpiService
from interface.controllers.kpi_controller import KpiController

app = Flask (__name__)

# TODO: Factory Pattern
connect(
  db='analysis',
  host='127.0.0.1',
  port=27017
)

kpi_repository: KpiCurrentStateRepository = KpiMongodbRepository()
kpi_service: KpiService = KpiService(kpi_repository)
kpi_controller: KpiController = KpiController(kpi_service)

app.register_blueprint(kpi_controller.get_blueprint(), url_prefix='/v1')

if __name__ == '__main__':
  app.run(debug = True)
