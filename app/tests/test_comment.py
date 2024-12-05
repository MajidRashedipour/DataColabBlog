from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def test_create_comment():
    login_response = client.post('/auth/login/', json={'email': 'testuser@gmail.com', 'password': 'dsfsdfasd'})
    data = login_response.json()
    access_token = f"Bearer {data['token']['Access']}"

    response = client.post('/comments/1/', json={'content': 'Content of My Blog Post'}, headers={'Authorization': access_token})
    assert response.status_code == 201
    assert response.json()['success'] == True

def test_read_post_comments():
    response = client.get('/comments/1/')
    assert response.status_code == 200
