from threading import Thread
from flask import Flask
from kafka.consumer.group import KafkaConsumer
from mongoengine import connect
from kafka import KafkaProducer
from bson import json_util

# Ports
from application.services.projections.kpi_current_state import KpiCurrentStateRepository, KpiCurrentStateService
from application.bounded_contexts.analysis.domain.model.kpi import KpiService
from application.services.dtos.event_dto import EventDtoProducer

# Driven Adapters
from application.services.kpi_service_v1 import KpiServiceV1
from application.services.kpi_current_state_service_v1 import KpiCurrentStateServiceV1
from infrastructure.brokers.consumers.other_sources_kafka_consumer import OtherSourcesKafkaConsumer
from infrastructure.repositories.projections.kpi_current_state_mongodb import KpiCurrentStateMongodbRepository
from infrastructure.brokers.producers.event_dto_kafka_producer import EventDtoKafkaProducer

# Driving Adapters
from interface.controllers.kpi_controller import KpiController
from infrastructure.brokers.consumers.kpi_current_state_kafka_consumer import KpiCurrentStateKafkaConsumer

# TODO: Factory Pattern
# TODO: Error handdling
# TODO: Defensive programming

def create_app():

  app = Flask (__name__)


  # MongoDB Config
  connect(
    db='analysis',
    host='127.0.0.1',
    port=27017
  )


  # Kafka Producer Config
  kafka_producer: KafkaProducer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],
    value_serializer=json_serializer
  )

  event_dto_producer: EventDtoProducer = EventDtoKafkaProducer(kafka_producer)


  # Repositories Config
  kpi_current_state_repository: KpiCurrentStateRepository = KpiCurrentStateMongodbRepository()


  # Services Config
  kpi_current_state_service: KpiCurrentStateService = KpiCurrentStateServiceV1(kpi_current_state_repository)
  kpi_service: KpiService = KpiServiceV1(kpi_current_state_service, event_dto_producer)


  # Controllers Config
  kpi_controller: KpiController = KpiController(kpi_service)


  # Start Controllers
  app.register_blueprint(kpi_controller.get_blueprint(), url_prefix='/v1')


  # Kafka Consumer Config
  kpi_current_state_consumer: KafkaConsumer = KafkaConsumer(
    'kpi',
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    group_id='kpi_current_state_kafka_consumer',
    value_deserializer=json_deserializer
  )

  other_sources_consumer: KafkaConsumer = KafkaConsumer(
    'other_sources',
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    group_id='other_sources_kafka_consumer',
    value_deserializer=json_deserializer
  )


  # Kafka Consumers as Threads Config
  create_kpi_current_state_consumer_thread: Thread = Thread(
    target = KpiCurrentStateKafkaConsumer(
      kpi_current_state_consumer,
      kpi_current_state_service
    )
  )

  other_sources_consumer_thread: Thread = Thread(
    target = OtherSourcesKafkaConsumer(
      other_sources_consumer,
      kpi_service
    )
  )


  # Start Threads
  create_kpi_current_state_consumer_thread.daemon = True
  create_kpi_current_state_consumer_thread.start()

  other_sources_consumer_thread.daemon = True
  other_sources_consumer_thread.start()


  return app


def json_serializer(data) -> str:
  return json_util.dumps(data.__dict__).encode("utf-8")

def json_deserializer(data) -> str:
  return json_util.loads(data)