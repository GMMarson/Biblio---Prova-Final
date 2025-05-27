from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from . import db

users_bp = Blueprint('users', __name__)

# Middleware de autorização para bibliotecário
def is_bibliotecario(user_id):
    usuario = db.usuarios.find_one({"_id": ObjectId(user_id)})
    return usuario and usuario["tipo"] == "bibliotecario"

# Aluno solicita cadastro
@users_bp.route("/solicitar-cadastro", methods=["POST"])
def solicitar_cadastro():
    data = request.json
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({"msg": "Campos obrigatórios"}), 400

    if db.usuarios.find_one({"email": email}):
        return jsonify({"msg": "Email já em uso"}), 400

    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": generate_password_hash(senha),
        "tipo": "aluno",
        "ativo": False
    }

    db.usuarios.insert_one(novo_usuario)
    return jsonify({"msg": "Solicitação enviada"}), 201

# Bibliotecário lista usuários pendentes
@users_bp.route("/usuarios/pendentes", methods=["GET"])
@jwt_required()
def listar_pendentes():
    user_id = get_jwt_identity()
    if not is_bibliotecario(user_id):
        return jsonify({"msg": "Acesso negado"}), 403

    pendentes = list(db.usuarios.find({"ativo": False, "tipo": "aluno"}))
    for u in pendentes:
        u["_id"] = str(u["_id"])
    return jsonify(pendentes), 200

# Aprovar ou rejeitar aluno
@users_bp.route("/usuarios/avaliar/<user_id>", methods=["POST"])
@jwt_required()
def avaliar_usuario(user_id):
    autor_id = get_jwt_identity()
    if not is_bibliotecario(autor_id):
        return jsonify({"msg": "Acesso negado"}), 403

    data = request.json
    aprovar = data.get("aprovar")

    if aprovar:
        db.usuarios.update_one({"_id": ObjectId(user_id)}, {"$set": {"ativo": True}})
        return jsonify({"msg": "Usuário aprovado"}), 200
    else:
        db.usuarios.delete_one({"_id": ObjectId(user_id)})
        return jsonify({"msg": "Usuário rejeitado"}), 200

@users_bp.route("/usuarios/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    usuario = db.usuarios.find_one({"_id": ObjectId(user_id)})
    if not usuario:
        return jsonify({"msg": "Usuário não encontrado"}), 404
    return jsonify({"nome": usuario["nome"], "tipo": usuario["tipo"]}), 200

@users_bp.route("/usuarios/<user_id>", methods=["PUT"])
@jwt_required()
def atualizar_usuario(user_id):
    usuario = db.usuarios.find_one({"_id": ObjectId(user_id)})
    if not usuario:
        return jsonify({"msg": "Usuário não encontrado"}), 404

    data = request.json
    atualizacao = {
        "nome": data.get("nome", usuario["nome"]),
        "email": data.get("email", usuario["email"]),
    }

    if "senha" in data and data["senha"]:
        from werkzeug.security import generate_password_hash
        atualizacao["senha"] = generate_password_hash(data["senha"])

    db.usuarios.update_one({"_id": ObjectId(user_id)}, {"$set": atualizacao})
    return jsonify({"msg": "Usuário atualizado"}), 200
