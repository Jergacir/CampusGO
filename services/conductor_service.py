from database import get_connection
from repositories.conductor_repository import ConductorRepository
from services.cloudinary_service import eliminar_imagen, subir_imagen


class ConductorService:

    def obtener_vehiculo(self, usuario_id):
        connection = get_connection()
        try:
            vehiculo = ConductorRepository(connection).obtener_vehiculo_por_usuario(
                usuario_id
            )
            if vehiculo is None:
                return None, "El usuario no posee perfil de conductor", 403
            return vehiculo, "Vehículo obtenido correctamente", 200
        finally:
            connection.close()

    def actualizar_vehiculo(self, usuario_id, datos):
        connection = get_connection()
        try:
            repository = ConductorRepository(connection)
            vehiculo = repository.obtener_vehiculo_por_usuario(usuario_id)
            if vehiculo is None:
                return None, "El usuario no posee perfil de conductor", 403

            repository.actualizar_vehiculo(usuario_id, datos)
            connection.commit()
            return datos, "Vehículo actualizado correctamente", 200
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def actualizar_foto(self, usuario_id, archivo):
        if archivo is None or not archivo.filename:
            return None, "Debe enviar una imagen en el campo 'foto'", 400

        if not (archivo.mimetype or "").startswith("image/"):
            return None, "El archivo debe ser una imagen", 415

        connection = get_connection()
        nuevo = None
        try:
            repository = ConductorRepository(connection)
            vehiculo = repository.obtener_vehiculo_por_usuario(usuario_id)
            if vehiculo is None:
                return None, "El usuario no posee perfil de conductor", 403

            nuevo = subir_imagen(
                archivo,
                "campusgo/vehiculos",
                f"conductor_{usuario_id}_auto",
            )
            repository.actualizar_foto_vehiculo(
                usuario_id,
                nuevo["url"],
                nuevo["public_id"],
            )
            connection.commit()

            anterior = vehiculo.get("foto_auto_public_id")
            if anterior and anterior != nuevo["public_id"]:
                eliminar_imagen(anterior)

            return nuevo, "Foto del vehículo actualizada correctamente", 200
        except Exception:
            connection.rollback()
            if nuevo:
                try:
                    eliminar_imagen(nuevo["public_id"])
                except Exception:
                    pass
            raise
        finally:
            connection.close()