import pytest
import json
from datetime import datetime
from app import create_app
from app.routes import weather_data

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_collect_weather(client, monkeypatch):
    # Mocking the OpenWeather API response
    def mock_get(url):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if "city_id_1" in url:
            return MockResponse({
                'id': 'city_id_1',
                'main': {
                    'temp': 20,
                    'humidity': 60
                }
            }, 200)
        elif "city_id_2" in url:
            return MockResponse({
                'id': 'city_id_2',
                'main': {
                    'temp': 25,
                    'humidity': 70
                }
            }, 200)
        return MockResponse(None, 404)

    monkeypatch.setattr('requests.get', mock_get)

    # Making the POST request to collect weather data
    response = client.post('/weather', data=json.dumps({
        'user_id': 'user_1',
        'city_ids': ['city_id_1', 'city_id_2']
    }), content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'Dados coletados'
    assert len(data['data']['cities']) == 2

def test_collect_weather_user_already_exists(client):
    weather_data['user_1'] = {
        'datetime': datetime.now(),
        'cities': [],
        'total': 2
    }

    response = client.post('/weather', data=json.dumps({
        'user_id': 'user_1',
        'city_ids': ['city_id_1', 'city_id_2']
    }), content_type='application/json')

    assert response.status_code == 409
    data = json.loads(response.data)
    assert data['status'] == 'Usuário já cadastrado'

def test_get_progress(client):
    weather_data['user_1'] = {
        'datetime': datetime.now(),
        'cities': [
            {'city_id': 'city_id_1', 'temperature': 20, 'humidity': 60},
            {'city_id': 'city_id_2', 'temperature': 25, 'humidity': 70}
        ],
        'total': 2
    }

    response = client.get('/progress/user_1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Progresso' in data
    assert data['Progresso'] == "100.00%"

def test_get_progress_user_not_found(client):
    response = client.get('/progress/non_existent_user')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Usuário não encontrado'
