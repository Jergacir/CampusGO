from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from services.conductor_service import ConductorService
from utils.response import error_response, success_response


conductor_bp = Blueprint("conductores", __name__)


@conductor_bp.route("/api/conductor/auto", methods=["GET"])
@jwt_required()
def obtener_vehiculo():
    data, message, code = ConductorService().obtener_vehiculo(
        get_jwt_identity()
    )
    if data is None:
        return error_response(message, code)
    return success_response(data, message, code)


@conductor_bp.route("/api/conductor/auto", methods=["PUT"])
@jwt_required()
def actualizar_vehiculo():
    datos = request.get_json(silent=True) or {}
    data, message, code = ConductorService().actualizar_vehiculo(
        get_jwt_identity(),
        datos,
    )
    if data is None:
        return error_response(message, code)
    return success_response(data, message, code)


@conductor_bp.route("/api/conductor/auto/foto", methods=["POST"])
@jwt_required()
def actualizar_foto_vehiculo():
    archivo = request.files.get("foto")
    data, message, code = ConductorService().actualizar_foto(
        get_jwt_identity(),
        archivo,
    )
    if data is None:
        return error_response(message, code)
    return success_response(data, message, code)