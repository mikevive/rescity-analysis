import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from flask import Flask
from flask_injector import FlaskInjector
from dependencies import configure
from mongoengine import connect

# Driving Adapters
from interface.controllers.kpi_controller import kpi_controller
from interface.controllers.kpi_group_controller import kpi_group_controller
from infrastructure.brokers.consumers.kpi_current_state_kafka_consumer import KpiCurrentStateKafkaConsumer
from infrastructure.brokers.consumers.kpi_group_current_state_kafka_consumer import KpiGroupCurrentStateKafkaConsumer
from infrastructure.brokers.consumers.other_sources_kafka_consumer import OtherSourcesKafkaConsumer



# TODO: Inject Mappers
# TODO: When to use mapper and when to instantiate a DTO?
# TODO: Projection as DTO?
# TODO: Flask Config Enviroments
# TODO: Error handdling
# TODO: Defensive programming
# TODO: Testing

def create_app():

  app = Flask (__name__)

  # Start MongoDB Connection
  connect(
    host=os.environ.get('MONGO_HOST'),
    port=int(os.environ.get('MONGO_PORT')),
    db=os.environ.get('MONGO_DB')
  )

  # Start Controllers
  app.register_blueprint(kpi_controller, url_prefix='/v1')
  app.register_blueprint(kpi_group_controller, url_prefix='/v1')

  flask_injector = FlaskInjector(app=app, modules=[configure])

  # Start Kafka Consumers
  flask_injector.injector.get(KpiCurrentStateKafkaConsumer)
  flask_injector.injector.get(KpiGroupCurrentStateKafkaConsumer)
  flask_injector.injector.get(OtherSourcesKafkaConsumer)

  return app
