import threading
from flask import Flask
from kafka.consumer.group import KafkaConsumer
from mongoengine import connect
from kafka import KafkaProducer
from bson import json_util

# Ports
from application.bounded_contexts.analysis.domain.projections.kpi_current_state import KpiCurrentStateRepository, KpiCurrentStateService
from application.bounded_contexts.analysis.domain.model.kpi import KpiService
from application.bounded_contexts.analysis.domain.model.event import EventProducer

# Driven Adapters
from application.services.kpi_service_v1 import KpiServiceV1
from application.services.kpi_current_state_service_v1 import KpiCurrentStateServiceV1
from infrastructure.repositories.projections.kpi_current_state_mongodb import KpiCurrentStateMongodbRepository
from infrastructure.brokers.producers.event_kafka_producer import EventKafkaProducer

# Driving Adapters
from interface.controllers.kpi_controller import KpiController
from infrastructure.brokers.consumers.kpi_current_state_kafka_consumer import KpiCurrentStateKafkaConsumer

app = Flask (__name__)

# TODO: Factory Pattern


# MongoDB Config
connect(
  db='analysis',
  host='127.0.0.1',
  port=27017
)


# Kafka Event Producer Config
def json_serializer(data) -> str:
  return json_util.dumps(data.__dict__).encode("utf-8")

kafka_producer: KafkaProducer = KafkaProducer(
  bootstrap_servers=['127.0.0.1:9092'],
  value_serializer=json_serializer
)

event_producer: EventProducer = EventKafkaProducer(kafka_producer)


def json_deserializer(data) -> str:
  return json_util.loads(data)

# Kpi Current State Consumer Config
def create_kpi_current_state_consumer():
  kpi_current_state_consumer: KafkaConsumer = KafkaConsumer(
    'analysis',
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    group_id='kpi_current_state_kafka_consumer',
    value_deserializer=json_deserializer
  )
  kpi_current_state_repository: KpiCurrentStateRepository = KpiCurrentStateMongodbRepository()
  kpi_current_state_service: KpiCurrentStateService = KpiCurrentStateServiceV1(kpi_current_state_repository)

  KpiCurrentStateKafkaConsumer(
    kpi_current_state_consumer,
    kpi_current_state_service
  )

# Kpi Controller Config
kpi_service: KpiService = KpiServiceV1(event_producer)
kpi_controller: KpiController = KpiController(kpi_service)


# Start Consumers
threading.Thread(target=create_kpi_current_state_consumer).start()


# Start Controllers
app.register_blueprint(kpi_controller.get_blueprint(), url_prefix='/v1')

if __name__ == '__main__':
  app.run(debug = True)
