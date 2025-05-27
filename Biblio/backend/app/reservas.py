from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from . import db
import qrcode
import io

reservas_bp = Blueprint('reservas', __name__)

# Verifica se é bibliotecário
def is_bibliotecario(user_id):
    usuario = db.usuarios.find_one({"_id": ObjectId(user_id)})
    return usuario and usuario["tipo"] == "bibliotecario"

# Solicitar reserva (aluno)
@reservas_bp.route("/reservas", methods=["POST"])
@jwt_required()
def solicitar_reserva():
    user_id = get_jwt_identity()
    data = request.json
    livro_id = data.get("livro_id")

    livro = db.livros.find_one({"_id": ObjectId(livro_id)})
    if not livro:
        return jsonify({"msg": "Livro não encontrado"}), 404

    reserva = {
        "livro_id": livro_id,
        "usuario_id": user_id,
        "aprovada": False
    }

    db.reservas.insert_one(reserva)
    return jsonify({"msg": "Reserva solicitada"}), 201

# Listar reservas pendentes (bibliotecário)
@reservas_bp.route("/reservas/pendentes", methods=["GET"])
@jwt_required()
def listar_pendentes():
    user_id = get_jwt_identity()
    if not is_bibliotecario(user_id):
        return jsonify({"msg": "Acesso negado"}), 403

    pendentes = list(db.reservas.find({"aprovada": False}))
    for r in pendentes:
        r["_id"] = str(r["_id"])
        r["usuario_id"] = str(r["usuario_id"])

        usuario = db.usuarios.find_one({"_id": ObjectId(r["usuario_id"])})
        livro = db.livros.find_one({"_id": ObjectId(r["livro_id"])})

        r["usuario_nome"] = usuario["nome"] if usuario else "Desconhecido"
        r["livro_nome"] = livro["titulo"] if livro else "Livro removido"
    return jsonify(pendentes), 200

# Aprovar reserva
@reservas_bp.route("/reservas/aprovar/<reserva_id>", methods=["POST"])
@jwt_required()
def aprovar_reserva(reserva_id):
    user_id = get_jwt_identity()
    if not is_bibliotecario(user_id):
        return jsonify({"msg": "Acesso negado"}), 403

    db.reservas.update_one(
        {"_id": ObjectId(reserva_id)},
        {"$set": {"aprovada": True}}
    )
    return jsonify({"msg": "Reserva aprovada"}), 200

# Obter QR Code da reserva aprovada
@reservas_bp.route("/reservas/qrcode/<reserva_id>", methods=["GET"])
@jwt_required()
def gerar_qrcode(reserva_id):
    reserva = db.reservas.find_one({"_id": ObjectId(reserva_id), "aprovada": True})
    if not reserva:
        return jsonify({"msg": "Reserva não encontrada ou não aprovada"}), 404

    dados = f"Reserva confirmada: Livro ID {reserva['livro_id']}, Usuário ID {reserva['usuario_id']}"
    qr = qrcode.make(dados)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@reservas_bp.route("/minhas-reservas", methods=["GET"])
@jwt_required()
def minhas_reservas():
    user_id = get_jwt_identity()
    reservas = list(db.reservas.find({"usuario_id": user_id}))
    for r in reservas:
        r["_id"] = str(r["_id"])
    return jsonify(reservas), 200
