import requests
import logging
from functools import lru_cache

logging.basicConfig(level=logging.INFO)

@lru_cache(maxsize=100)
def obter_coordenadas(cidade, estado):
    """Obtém coordenadas geográficas usando a API do OpenStreetMap."""
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'city': cidade,
        'state': estado,
        'country': 'Brazil',
        'format': 'json'
    }
    headers = {
        'User-Agent': 'MeuProjeto/1.0 (suporte@alphaeletrica.ind.br)'
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter coordenadas para {cidade}, {estado}: {e}")
    return None, None

def validar_tecnico(dados):
    """Valida os dados de um técnico."""
    campos_obrigatorios = ['nome', 'cidade', 'estado', 'empresa']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return False, f"Campo {campo} é obrigatório"
    return True, None