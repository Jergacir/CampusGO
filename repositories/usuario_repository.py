class UsuarioRepository:

    def __init__(self, connection):
        self.connection = connection

    def buscar_por_email(self, email):
        cursor = self.connection.cursor()

        try:
            sql = """
                SELECT 
                    id, 
                    email, 
                    password_hash, 
                    nombres, 
                    apellidos, 
                    rol, 
                    estado 
                FROM usuario 
                WHERE email = %s 
                LIMIT 1
            """

            cursor.execute(sql, (email,))
            return cursor.fetchone()

        finally:
            cursor.close()

    def buscar_por_id(self, usuario_id):
        cursor = self.connection.cursor()

        try:
            sql = """
                SELECT 
                    id, 
                    email, 
                    nombres, 
                    apellidos, 
                    rol, 
                    estado, 
                    fecha_registro,
                    foto_url
                FROM usuario 
                WHERE id = %s 
                LIMIT 1
            """

            cursor.execute(sql, (usuario_id,))
            return cursor.fetchone()

        finally:
            cursor.close()

    def obtener_foto_por_usuario(self, usuario_id):
        """
        Devuelve únicamente los datos necesarios para autorizar
        y localizar la foto del usuario autenticado.
        """
        cursor = self.connection.cursor()
        try:
            sql = """
                SELECT id, foto, foto_url, foto_public_id, estado
                FROM usuario
                WHERE id = %s
                LIMIT 1
            """
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def actualizar_foto(self, usuario_id, foto_url, foto_public_id):
        cursor = self.connection.cursor()
        try:
            sql = """
                UPDATE usuario
                SET foto_url = %s,
                    foto_public_id = %s
                WHERE id = %s
            """
            cursor.execute(sql, (foto_url, foto_public_id, usuario_id))
        finally:
            cursor.close()
    