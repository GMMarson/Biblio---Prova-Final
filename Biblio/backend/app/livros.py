from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from . import db

livros_bp = Blueprint('livros', __name__)

# Verifica se o usuário logado é bibliotecário
def is_bibliotecario(user_id):
    usuario = db.usuarios.find_one({"_id": ObjectId(user_id)})
    return usuario and usuario["tipo"] == "bibliotecario"

# Listar todos os livros
@livros_bp.route("/livros", methods=["GET"])
@jwt_required()
def listar_livros():
    livros = list(db.livros.find())
    for livro in livros:
        livro["_id"] = str(livro["_id"])
    return jsonify(livros), 200

# Cadastrar livro (apenas bibliotecário)
@livros_bp.route("/livros", methods=["POST"])
@jwt_required()
def adicionar_livro():
    user_id = get_jwt_identity()
    if not is_bibliotecario(user_id):
        return jsonify({"msg": "Acesso negado"}), 403

    data = request.json
    titulo = data.get("titulo")
    autor = data.get("autor")
    ano = data.get("ano")
    genero = data.get("genero")
    quantidade = data.get("quantidade")

    if not all([titulo, autor, ano, genero, quantidade]):
        return jsonify({"msg": "Todos os campos são obrigatórios"}), 400

    livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "genero": genero,
        "quantidade": quantidade
    }

    db.livros.insert_one(livro)
    return jsonify({"msg": "Livro cadastrado"}), 201

# Deletar livro (bibliotecário)
@livros_bp.route("/livros/<livro_id>", methods=["DELETE"])
@jwt_required()
def deletar_livro(livro_id):
    user_id = get_jwt_identity()
    if not is_bibliotecario(user_id):
        return jsonify({"msg": "Acesso negado"}), 403

    db.livros.delete_one({"_id": ObjectId(livro_id)})
    return jsonify({"msg": "Livro removido"}), 200
