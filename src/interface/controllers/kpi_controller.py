from flask import Blueprint, request, Response
from bson import json_util
from injector import inject

from application.services.dtos.kpi_create_dto import KpiCreateDto
from application.services.dtos.kpi_created_dto import KpiCreatedDto
from application.services.dtos.kpi_update_dto import KpiUpdateDto
from application.services.dtos.error_dto import ErrorDto
from application.bounded_contexts.analysis.domain.model.kpi import KpiService
from infrastructure.repositories.exceptions.exceptions import KpiNotFoundError

kpi_controller = Blueprint('kpi_controller', __name__)


@inject
@kpi_controller.route('/kpis', methods=['POST'])
def create(kpi_service: KpiService):
  name: str = request.json['name']
  equation: str = request.json['equation']
  units: str = request.json['units']

  try:
    kpi_create_dto: KpiCreateDto = KpiCreateDto(name, equation, units)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 400)

  kpi_created_dto: KpiCreatedDto = kpi_service.create(kpi_create_dto)

  response = json_util.dumps(kpi_created_dto.__dict__)
  return Response(response, mimetype = 'application/json', status = 202)


@inject
@kpi_controller.route('/kpis/<id>', methods=['PUT'])
def update(kpi_service: KpiService, id):
  name: str = request.json['name']
  equation: str = request.json['equation']
  units: str = request.json['units']

  try:
    kpi_update_dto = KpiUpdateDto(id, name, equation, units)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 400)

  try:
    kpi_service.update(kpi_update_dto)
  except KpiNotFoundError as error:
    code, message, description = error.args

    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 404)

  return Response(mimetype = 'application/json', status = 202)


@inject
@kpi_controller.route('/kpis/<id>', methods=['DELETE'])
def delete(kpi_service: KpiService, id):

  try:
    kpi_created_dto = KpiCreatedDto(id)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 400)

  try:
    kpi_service.delete(kpi_created_dto)
  except KpiNotFoundError as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 404)

  return Response(mimetype = 'application/json', status = 202)
