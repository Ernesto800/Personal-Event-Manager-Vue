from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_jwt_token(user_id):
    if not isinstance(user_id, int):
        print(f"ERROR: generate_jwt_token recibió un user_id no entero: {user_id} (Tipo: {type(user_id)})")
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            print("ERROR: No se pudo convertir user_id a entero. Esto causará problemas.")
            return None 

    expires = timedelta(hours=24)
    access_token = create_access_token(identity=user_id, expires_delta=expires)
    print(f"DEBUG: Token generado para user_id: {user_id} (Tipo: {type(user_id)})")
    return access_token

