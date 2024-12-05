from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def test_create_post():
    login_response = client.post('/auth/login/', json={'email': 'testuser@gmail.com', 'password': 'dsfsdfasd'})
    data = login_response.json()
    access_token = f"Bearer {data['token']['Access']}"

    response = client.post('/', json={'title': 'My Blog Post', 'content': 'Content of My Blog Post', 'tags': ['tag', 'post', 'blog']}, headers={'Authorization': access_token})
    assert response.status_code == 201
    assert response.json()['success'] == True

def test_read_posts():
    response = client.get('/')
    assert response.status_code == 200
