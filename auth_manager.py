import hashlib

class AuthManager:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def encriptar_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verificar_password(self, password, password_encriptada):
        return self.encriptar_password(password) == password_encriptada

    def generar_token(self, usuario_id, email):
        import jwt
        import datetime
        payload = {
            'id': usuario_id,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        }
        return jwt.encode(payload, 'clave_secreta_123', algorithm='HS256')

    def verificar_token(self, token):
        import jwt
        try:
            return jwt.decode(token, 'clave_secreta_123', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

# Singleton — siempre la misma instancia
auth = AuthManager()