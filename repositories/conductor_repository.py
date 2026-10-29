class ConductorRepository:

    def __init__(self, connection):
        self.connection = connection

    def obtener_vehiculo_por_usuario(self, usuario_id):
        cursor = self.connection.cursor()
        try:
            sql = """
                SELECT id, marca_auto, modelo_auto, placa_auto,
                       color_auto, foto_auto_url, foto_auto_public_id
                FROM conductor
                WHERE usuario_id = %s
                LIMIT 1
            """
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def actualizar_vehiculo(self, usuario_id, datos):
        cursor = self.connection.cursor()
        try:
            sql = """
                UPDATE conductor
                SET marca_auto = %s,
                    modelo_auto = %s,
                    placa_auto = %s,
                    color_auto = %s
                WHERE usuario_id = %s
            """
            cursor.execute(sql, (
                datos.get("marca_auto"),
                datos.get("modelo_auto"),
                datos.get("placa_auto"),
                datos.get("color_auto"),
                usuario_id,
            ))
            return cursor.rowcount
        finally:
            cursor.close()

    def actualizar_foto_vehiculo(self, usuario_id, foto_url, foto_public_id):
        cursor = self.connection.cursor()
        try:
            sql = """
                UPDATE conductor
                SET foto_auto_url = %s,
                    foto_auto_public_id = %s
                WHERE usuario_id = %s
            """
            cursor.execute(sql, (foto_url, foto_public_id, usuario_id))
            return cursor.rowcount
        finally:
            cursor.close()