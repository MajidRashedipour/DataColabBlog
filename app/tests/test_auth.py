from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def test_create_user():
    response = client.post('/auth/register/', json={'email': 'testuser@gmail.com', 'password': 'dsfsdfasd', 'confirm_password': 'dsfsdfasd'})
    assert response.status_code == 201
    assert response.json()['success'] == True

def test_create_existing_user():
    response = client.post('/auth/register/', json={'email': 'user@gmail.com', 'password': 'dsfsdfasd', 'confirm_password': 'dsfsdfasd'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Email already exist'}

def test_login_user():
    response = client.post('/auth/login/', json={'email': 'user@gmail.com', 'password': 'dsfsdfasd'})
    assert response.status_code == 200
    assert response.json()['success'] == True

def test_logout_user():
    login_response = client.post('/auth/login/', json={'email': 'user@gmail.com', 'password': 'dsfsdfasd'})
    data = login_response.json()
    access_token = f"Bearer {data['token']['Access']}"
    response = client.post('/auth/logout/', headers={'Authorization': access_token})
    assert response.status_code == 200
    assert response.json()['success'] == True
