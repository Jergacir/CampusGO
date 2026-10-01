from database import get_connection
from repositories.viaje_repository import ViajeRepository
from datetime import timedelta, date, datetime


class ViajeService:

    def crear(self, usuario_id, datos):
        obligatorios = ["origen", "destino", "fecha", "hora", "cupos", "precio"]

        if any(campo not in datos for campo in obligatorios):
            return None, "Faltan datos obligatorios", 400

        if int(datos["cupos"]) <= 0:
            return None, "Los cupos deben ser mayores que cero", 400

        if float(datos["precio"]) < 0:
            return None, "El precio no puede ser negativo", 400

        connection = get_connection()

        try:
            repository = ViajeRepository(connection)
            conductor_id = repository.obtener_conductor_id_por_usuario(usuario_id)

            if conductor_id is None:
                return None, "El usuario no posee perfil de conductor", 403

            if repository.existe_viaje_duplicado(conductor_id, datos["fecha"], datos["hora"], datos["origen"], datos["destino"]):
                return None, "Ya tiene un viaje programado para la misma fecha, hora y ruta", 409

            viaje_id = repository.crear(conductor_id, datos)
            connection.commit()

            return {"viaje_id": viaje_id}, "Viaje creado correctamente", 201

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def listar(self, filtros):
        p_min = filtros.get("precio_min")
        p_max = filtros.get("precio_max")

        # Validar numéricos
        try:
            p_min_num = float(p_min) if p_min is not None else None
            p_max_num = float(p_max) if p_max is not None else None
        except ValueError:
            return None, "Los filtros de precio deben ser valores numéricos", 400

        # Validar rango
        if p_min_num is not None and p_max_num is not None:
            if p_min_num > p_max_num:
                return None, "precio_min no puede ser mayor que precio_max", 400

        # Fecha mínima
        desde_val = filtros.get("desde")
        if desde_val:
            try:
                datetime.strptime(desde_val, "%Y-%m-%d")
            except ValueError:
                return None, "El formato de fecha 'desde' debe ser YYYY-MM-DD", 400

        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viajes = repository.listar(
                filtros.get("origen"),
                filtros.get("destino"),
                filtros.get("fecha"),
                filtros.get("estado"),
                precio_min=p_min_num,
                precio_max=p_max_num,
                desde=filtros.get("desde"),
                solo_disponibles=filtros.get("solo_disponibles", False)
            )

            for viaje in viajes:
                if isinstance(viaje.get("hora"), timedelta):
                    viaje["hora"] = str(viaje["hora"])
                if viaje.get("fecha") and hasattr(viaje["fecha"], "strftime"):
                    viaje["fecha"] = viaje["fecha"].strftime("%Y-%m-%d")
                if viaje.get("precio") is not None:
                    viaje["precio"] = float(viaje["precio"])

            return viajes, "Viajes obtenidos correctamente", 200
        finally:
            connection.close()

    def obtener(self, viaje_id):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)

            if viaje is None:
                return None, "Viaje no encontrado", 404

            if isinstance(viaje.get("hora"), timedelta):
                viaje["hora"]=str(viaje["hora"])

            if isinstance(viaje.get("fecha"), date):
                viaje["fecha"]=viaje["fecha"].isoformat()

            return viaje, "Viaje obtenido correctamente", 200
        finally:
            connection.close()

    def actualizar(self, usuario_id, viaje_id, datos):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)

            if viaje is None:
                return None, "Viaje no encontrado", 404

            if str(viaje["conductor_usuario_id"]) != str(usuario_id):
                return None, "No puede modificar un viaje de otro conductor", 403

            if viaje["estado"] in ("FINALIZADO", "CANCELADO"):
                return None, "El estado actual no permite modificar el viaje", 409

            repository.actualizar(viaje_id, datos)
            connection.commit()

            return {"viaje_id": viaje_id}, "Viaje actualizado correctamente", 200

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def cancelar(self, usuario_id, viaje_id):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)

            if viaje is None:
                return None, "Viaje no encontrado", 404

            if str(viaje["conductor_usuario_id"]) != str(usuario_id):
                return None, "No puede cancelar un viaje de otro conductor", 403

            if viaje["estado"] == "CANCELADO":
                return None, "El viaje ya se encuentra cancelado", 409

            repository.cancelar(viaje_id)
            connection.commit()

            return {"viaje_id": viaje_id}, "Viaje cancelado correctamente", 200

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def listar_mios(self, usuario_id, estado=None):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            conductor_id = repository.obtener_conductor_id_por_usuario(usuario_id)

            if conductor_id is None:
                return None, "El usuario no posee perfil de conductor", 403

            viajes = repository.listar_por_conductor(conductor_id, estado)

            for v in viajes:
                if isinstance(v.get("hora"), timedelta):
                    v["hora"] = str(v["hora"])
                if v.get("fecha") and hasattr(v["fecha"], "strftime"):
                    v["fecha"] = v["fecha"].strftime("%Y-%m-%d")
                if v.get("precio") is not None:
                    v["precio"] = float(v["precio"])

            return viajes, "Mis viajes obtenidos correctamente", 200
        finally:
            connection.close()

    def actualizar_cupos(self, usuario_id, viaje_id, datos):
        cupos = datos.get("cupos")

        if cupos is None or not isinstance(cupos, int) or cupos < 0:
            return None, "El número de cupos debe ser un entero mayor o igual a cero", 400

        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)

            if viaje is None:
                return None, "Viaje no encontrado", 404

            if str(viaje["conductor_usuario_id"]) != str(usuario_id):
                return None, "No puede modificar un viaje de otro conductor", 403

            if viaje["estado"] in ("FINALIZADO", "CANCELADO"):
                return None, "El estado actual no permite modificar los cupos", 409

            repository.actualizar_cupos(viaje_id, cupos)
            connection.commit()

            return {"viaje_id": viaje_id, "cupos": cupos}, "Cupos actualizados correctamente", 200
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    ESTADOS_PERMITIDOS = {"DISPONIBLE", "EN_CURSO", "FINALIZADO", "CANCELADO"}

    def cambiar_estado(self, usuario_id, viaje_id, datos):
        nuevo_estado = datos.get("estado")

        if nuevo_estado not in self.ESTADOS_PERMITIDOS:
            return None, f"Estado inválido. Permitidos: {self.ESTADOS_PERMITIDOS}", 400

        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)

            if viaje is None:
                return None, "Viaje no encontrado", 404

            if str(viaje["conductor_usuario_id"]) != str(usuario_id):
                return None, "No posee permisos para alterar este viaje", 403

            estado_actual = viaje["estado"]

            # Reglas de transición de estado
            if estado_actual == "CANCELADO":
                return None, "Un viaje CANCELADO no puede cambiar de estado", 409
            if estado_actual == "FINALIZADO":
                return None, "Un viaje FINALIZADO no puede cambiar de estado", 409

            repository.actualizar_estado(viaje_id, nuevo_estado)
            connection.commit()

            return {"viaje_id": viaje_id, "nuevo_estado": nuevo_estado}, "Estado actualizado correctamente", 200
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def obtener_resumen(self, usuario_id):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            conductor_id = repository.obtener_conductor_id_por_usuario(usuario_id)

            if conductor_id is None:
                return None, "El usuario no posee perfil de conductor", 403

            resumen_raw = repository.obtener_resumen_por_estado(conductor_id)

            # Estructurar formato consumible para la App Móvil
            resumen = {item["estado"]: item["cantidad"] for item in resumen_raw}

            return resumen, "Resumen obtenido correctamente", 200
        finally:
            connection.close()
    