from flask import Blueprint, request, Response
from application.services.projections.kpi_current_state import KpiCurrentState
from application.bounded_contexts.analysis.domain.model.kpi import Kpi, KpiService
from bson import json_util, ObjectId

class KpiController:

  def __init__(self, kpi_service: KpiService):
    self._kpi_service: KpiService = kpi_service

  def get_blueprint(self):
    kpi_controller = Blueprint('kpi_controller', __name__)

    @kpi_controller.route('/kpi', methods=['POST'])
    def create():
      name: str = request.json['name']

      kpi_id: str = self._kpi_service.create(name)

      response = json_util.dumps({'id': kpi_id})
      return Response(response, mimetype = 'application/json', status = 202)

    @kpi_controller.route('/kpi/<id>', methods=['PUT'])
    def update_name(id):
      name: str = request.json['name']

      self._kpi_service.update_name(ObjectId(id), name)
      return Response(mimetype = 'application/json', status = 202)

    return kpi_controller





