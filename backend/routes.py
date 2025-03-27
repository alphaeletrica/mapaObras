from flask import Blueprint, request, jsonify, render_template
from flask import current_app
from backend.app import db
from backend.models import Tecnico
from backend.utils import obter_coordenadas, validar_tecnico

tecnico_bp = Blueprint('tecnicos', __name__, template_folder='templates')

@tecnico_bp.route('/')
def home():
    return render_template('index.html')

@tecnico_bp.route('/tecnicos', methods=['GET'])
def listar_tecnicos():
    tecnicos = Tecnico.query.all()
    return jsonify([tecnico.to_dict() for tecnico in tecnicos])

@tecnico_bp.route('/tecnicos', methods=['POST'])
def adicionar_tecnico():
    dados = request.json
    valido, erro = validar_tecnico(dados)
    if not valido:
        return jsonify({'erro': erro}), 400
    
    # Obtém as coordenadas com base na cidade e estado
    latitude, longitude = obter_coordenadas(dados['cidade'], dados['estado'])
    if latitude is None or longitude is None:
        return jsonify({'erro': 'Não foi possível obter coordenadas'}), 400
    
    # Cria o técnico com as coordenadas obtidas
    novo_tecnico = Tecnico(
        nome=dados['nome'],
        cidade=dados['cidade'],
        estado=dados['estado'],
        empresa=dados['empresa'],
        latitude=latitude,
        longitude=longitude
    )
    
    db.session.add(novo_tecnico)
    db.session.commit()
    return jsonify(novo_tecnico.to_dict()), 201

@tecnico_bp.route('/tecnicos/<int:id>', methods=['PUT'])
def atualizar_tecnico(id):
    tecnico = Tecnico.query.get_or_404(id)
    dados = request.json
    valido, erro = validar_tecnico(dados)
    if not valido:
        return jsonify({'erro': erro}), 400
    
    # Atualiza as coordenadas se a cidade ou estado forem alterados
    if 'cidade' in dados or 'estado' in dados:
        cidade = dados.get('cidade', tecnico.cidade)
        estado = dados.get('estado', tecnico.estado)
        latitude, longitude = obter_coordenadas(cidade, estado)
        if latitude and longitude:
            tecnico.latitude = latitude
            tecnico.longitude = longitude
    
    for key, value in dados.items():
        setattr(tecnico, key, value)
    
    db.session.commit()
    return jsonify(tecnico.to_dict())

@tecnico_bp.route('/tecnicos/<int:id>', methods=['DELETE'])
def deletar_tecnico(id):
    tecnico = Tecnico.query.get_or_404(id)
    db.session.delete(tecnico)
    db.session.commit()
    return '', 204

@tecnico_bp.route('/tecnicos/atualizar-coordenadas', methods=['POST'])
def atualizar_coordenadas():
    try:
        # Busca todos os técnicos sem latitude ou longitude
        tecnicos = Tecnico.query.filter(
            (Tecnico.latitude == None) | (Tecnico.longitude == None)).all()
        
        for tecnico in tecnicos:
            # Obtém as coordenadas com base na cidade e estado
            latitude, longitude = obter_coordenadas(tecnico.cidade, tecnico.estado)
            if latitude and longitude:
                tecnico.latitude = latitude
                tecnico.longitude = longitude
        
        db.session.commit()
        return jsonify({'mensagem': 'Coordenadas atualizadas com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500