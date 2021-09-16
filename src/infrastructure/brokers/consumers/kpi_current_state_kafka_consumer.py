from bson.objectid import ObjectId
from kafka import KafkaConsumer

from application.bounded_contexts.analysis.domain.projections.kpi_current_state import KpiCurrentState, KpiCurrentStateService

class KpiCurrentStateKafkaConsumer:

  def __init__(self, kafka_consumer: KafkaConsumer, kpi_current_state_service: KpiCurrentStateService) -> None:
    self._kafka_consumer: KafkaConsumer = kafka_consumer
    self._kpi_current_state_service: KpiCurrentStateService = kpi_current_state_service

    for event in self._kafka_consumer:
      id = event.value['aggregate_id']
      name = event.value['data']['name']
      print(f'>> Consumiendo {id} del topico {event.topic}')
      self._kpi_current_state_service.create(ObjectId(id), name)