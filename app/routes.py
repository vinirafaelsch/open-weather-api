import os

import requests
import asyncio

from dotenv import load_dotenv
from datetime import datetime

from flask import Blueprint, request, jsonify

bp = Blueprint('main', __name__)
weather_data = {}

load_dotenv()

token = os.getenv('OPENWEATHER_API_KEY')

@bp.route('/weather', methods=['POST'])
async def collect_weather():
    user_id = request.json['user_id']
    city_ids = request.json['city_ids']

    if user_id in weather_data:
        return jsonify({ "status": "Usuário já cadastrado" }), 409

    weather_data[user_id] = { 'datetime': datetime.now(), 'cities': [], 'total': len(city_ids) }

    for city_id in city_ids:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={token}&units=metric')
        if response.status_code == 200:
            json_data = response.json()
            new_city = {
                'city_id': json_data['id'],
                'temperature': json_data['main']['temp'],
                'humidity': json_data['main']['humidity']
            }
            weather_data[user_id]['cities'].append(new_city)
        await asyncio.sleep(1.2)  # Respeitar as 60 req por minuto
    
    return jsonify({ "status": "Dados coletados", "data": weather_data[user_id] }), 200

@bp.route('/progress/<user_id>', methods=['GET'])
def get_progress(user_id):
    if user_id in weather_data:
        collected = len(weather_data[user_id]['cities'])
        total = weather_data[user_id]['total']
        progress = (collected / total) * 100
        formated_progress = "{:.2%}".format(progress)
        return jsonify({ "Progresso": formated_progress }), 200
    else:
        return jsonify({ "error": "Usuário não encontrado" }), 404