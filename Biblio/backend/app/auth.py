from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"msg": "Campos obrigatórios"}), 400

    usuario = db.usuarios.find_one({"email": email})
    if not usuario or not check_password_hash(usuario["senha"], senha):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    token = create_access_token(identity=str(usuario["_id"]))
    return jsonify({
        "token": token,
        "user_id": str(usuario["_id"]),
        "tipo": usuario["tipo"]
    }), 200

@auth_bp.route("/registro", methods=["POST"])
def registro():
    data = request.json
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    tipo = data.get("tipo")  # aluno ou bibliotecario

    if not nome or not email or not senha or not tipo:
        return jsonify({"msg": "Campos obrigatórios"}), 400

    if db.usuarios.find_one({"email": email}):
        return jsonify({"msg": "Email já registrado"}), 400

    usuario = {
        "nome": nome,
        "email": email,
        "senha": generate_password_hash(senha),
        "tipo": tipo,
        "ativo": tipo == "bibliotecario"  # bibliotecário já entra ativo
    }

    result = db.usuarios.insert_one(usuario)
    return jsonify({"msg": "Usuário registrado", "id": str(result.inserted_id)}), 201
