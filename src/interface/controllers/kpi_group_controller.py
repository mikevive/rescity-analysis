from flask import Blueprint, request, Response
from bson import json_util
from injector import inject

from application.services.dtos.kpi_group_create_dto import KpiGroupCreateDto
from application.services.dtos.kpi_group_created_dto import KpiGroupCreatedDto
from application.services.dtos.kpi_group_update_dto import KpiGroupUpdateDto
from application.services.dtos.error_dto import ErrorDto
from application.bounded_contexts.analysis.domain.model.kpi_group import KpiGroupService

kpi_group_controller = Blueprint('kpi_group_controller', __name__)

@inject
@kpi_group_controller.route('/kpi-groups', methods=['POST'])
def create(kpi_group_service: KpiGroupService):
  name: str = request.json['name']
  kpis: str = request.json['kpis']

  try:
    kpi_group_create_dto: KpiGroupCreateDto = KpiGroupCreateDto(name, kpis)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 400)

  try:
    kpi_group_created_dto: KpiGroupCreatedDto = kpi_group_service.create(kpi_group_create_dto)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 404)

  response = json_util.dumps(kpi_group_created_dto.__dict__)
  return Response(response, mimetype = 'application/json', status = 202)


@inject
@kpi_group_controller.route('/kpi-groups/<id>', methods=['PUT'])
def update(kpi_group_service: KpiGroupService, id):
  name: str = request.json['name']
  kpis: str = request.json['kpis']

  try:
    kpi_group_update_dto = KpiGroupUpdateDto(id, name, kpis)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 400)

  try:
    kpi_group_service.update(kpi_group_update_dto)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 404)

  return Response(mimetype = 'application/json', status = 202)


@inject
@kpi_group_controller.route('/kpi-groups/<id>', methods=['DELETE'])
def delete(kpi_group_service: KpiGroupService, id):

  try:
    kpi_group_created_dto = KpiGroupCreatedDto(id)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 400)

  try:
    kpi_group_service.delete(kpi_group_created_dto)
  except Exception as error:
    code, message, description = error.args
    error_dto: ErrorDto = ErrorDto(code, message, description)
    error = json_util.dumps(error_dto.__dict__)
    return Response(error, mimetype = 'application/json', status = 404)

  return Response(mimetype = 'application/json', status = 202)
