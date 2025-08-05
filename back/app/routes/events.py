from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Event, User
from app import db
from datetime import datetime, time

events_bp = Blueprint('events_bp', __name__)

@events_bp.route('/events', methods=['GET'])
@jwt_required()
def get_user_events():
    try:
        current_user_id = None
        try:
            current_user_id = get_jwt_identity()
            print(f"DEBUG: get_user_events - current_user_id from JWT: {current_user_id} (Type: {type(current_user_id)})")
        except Exception as jwt_error:
            print(f"ERROR: get_user_events - Falló get_jwt_identity(): {jwt_error}")
            return jsonify({"message": "Error al obtener identidad del token."}), 401

        if not isinstance(current_user_id, int):
            print(f"ERROR: get_user_events - JWT identity is not an integer. Identity: {current_user_id}")
            return jsonify({"message": "Identidad de usuario inválida en el token. Se esperaba un ID numérico."}), 401

        user = User.query.get(current_user_id)
        print(f"DEBUG: get_user_events - User found: {user}")

        if not user:
            print("DEBUG: get_user_events - User not found in DB for this ID, returning 404")
            return jsonify({"message": "Usuario no encontrado"}), 404

        events = Event.query.filter_by(user_id=user.id).all()
        
        events_data = []
        for event in events:
            events_data.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'date': event.date.strftime('%Y-%m-%d'),
                'time': event.time.strftime('%H:%M') if event.time else None,
            })
        print("DEBUG: get_user_events - Events fetched successfully, returning 200")
        return jsonify({"events": events_data}), 200

    except Exception as e:
        print(f"ERROR: get_user_events - Excepción inesperada en la función: {e}")
        return jsonify({"message": f"Error interno del servidor al cargar eventos: {str(e)}"}), 500

@events_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    try:
        current_user_id = None
        try:
            current_user_id = get_jwt_identity()
            print(f"DEBUG: create_event - current_user_id from JWT: {current_user_id} (Type: {type(current_user_id)})")
        except Exception as jwt_error:
            print(f"ERROR: create_event - Falló get_jwt_identity(): {jwt_error}")
            return jsonify({"message": "Error al obtener identidad del token para crear evento."}), 401

        if not isinstance(current_user_id, int):
            print(f"ERROR: create_event - JWT identity is not an integer: {current_user_id}")
            return jsonify({"message": "Identidad de usuario inválida en el token. Se esperaba un ID numérico."}), 401

        user = User.query.get(current_user_id)
        print(f"DEBUG: create_event - User found: {user}")

        if not user:
            print("DEBUG: create_event - User not found, returning 404")
            return jsonify({"message": "Usuario no encontrado"}), 404

        data = request.get_json()
        print(f"DEBUG: create_event - Received data: {data}")

        title = data.get('title')
        description = data.get('description')
        date_str = data.get('date')
        time_str = data.get('time')

        if not title or not date_str:
            print("DEBUG: create_event - Missing title or date, returning 400")
            return jsonify({'message': 'Título y fecha son requeridos'}), 400

        # --- CAMBIO CRÍTICO AQUÍ: Usar fromisoformat para la fecha ---
        try:
            # Parsear la fecha completa ISO 8601 y luego extraer solo la parte de la fecha
            event_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date() 
            event_time = datetime.strptime(time_str, '%H:%M').time() if time_str else None
        except ValueError as ve:
            print(f"ERROR: create_event - Date/Time format error: {ve}")
            return jsonify({'message': 'Formato de fecha u hora inválido. Usa YYYY-MM-DDTHH:MM:SS.sssZ para fecha y HH:MM para hora.'}), 400
        # --- FIN CAMBIO CRÍTICO ---

        new_event = Event(
            title=title,
            description=description,
            date=event_date,
            time=event_time,
            user_id=user.id
        )
        db.session.add(new_event)
        db.session.commit()
        print("DEBUG: create_event - Event created successfully, returning 201")
        return jsonify({'message': 'Evento creado exitosamente', 'event': {
            'id': new_event.id,
            'title': new_event.title,
            'description': new_event.description,
            'date': new_event.date.strftime('%Y-%m-%d'),
            'time': new_event.time.strftime('%H:%M') if new_event.time else None,
        }}), 201

    except Exception as e:
        print(f"ERROR: create_event - Excepción inesperada en la función: {e}")
        return jsonify({"message": f"Error interno del servidor al crear evento: {str(e)}"}), 500


@events_bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    event = Event.query.filter_by(id=event_id, user_id=user.id).first()

    if not event:
        return jsonify({'message': 'Evento no encontrado o no autorizado'}), 404

    data = request.get_json()
    from datetime import datetime, time

    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    
    date_str = data.get('date')
    if date_str:
        # --- CAMBIO CRÍTICO AQUÍ: Usar fromisoformat para la fecha ---
        try:
            event.date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        except ValueError:
            return jsonify({'message': 'Formato de fecha inválido. Usa YYYY-MM-DDTHH:MM:SS.sssZ'}), 400
        # --- FIN CAMBIO CRÍTICO ---
    
    time_str = data.get('time')
    if time_str is not None:
        try:
            event.time = datetime.strptime(time_str, '%H:%M').time() if time_str else None
        except ValueError:
            return jsonify({'message': 'Formato de hora inválido. Usa HH:MM'}), 400

    db.session.commit()
    return jsonify({'message': 'Evento actualizado exitosamente', 'event': {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d'),
        'time': event.time.strftime('%H:%M') if event.time else None,
    }}), 200

@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    event = Event.query.filter_by(id=event_id, user_id=user.id).first()

    if not event:
        return jsonify({'message': 'Evento no encontrado o no autorizado'}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Evento eliminado exitosamente'}), 200