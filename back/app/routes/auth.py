from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from app.utils.auth_utils import generate_jwt_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    lastname = data.get('lastname')
    email = data.get('email')
    phone = data.get('phone')
    username = data.get('username')
    password = data.get('password')

    if not username or not password or not email:
        return jsonify({'message': 'Usuario, contraseña y email son requeridos'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'El nombre de usuario ya existe'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'El email ya está registrado'}), 409

    new_user = User(
        username=username,
        name=name,
        lastname=lastname,
        email=email,
        phone=phone
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    token = generate_jwt_token(new_user.id)
    return jsonify({
        'message': 'Usuario registrado exitosamente', 
        'token': token,
        'username': new_user.username
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    token = generate_jwt_token(user.id)
    return jsonify({
        'message': 'Inicio de sesión exitoso', 
        'token': token, 
        'username': user.username
    }), 200