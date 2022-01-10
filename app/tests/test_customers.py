from fastapi.testclient import TestClient

def test_create(client: TestClient):
    response = client.post('/customers/', json={
        'first_name': 'PRIMEIRO',
        'last_name': 'ULTIMO',
        'phone_number': '999999999',
        'genre': 'm',
        'document_id': 1,
        'birth_date':'2021-12-15',
        'user':{
            'display_name': 'DISPLAY',
            'email':'email@email.com',
            'password': '123',
            'role': 'user'
        }
    })
    assert response.status_code == 201
    assert response.json() == None
    response = client.get('/customers/1')
    assert response.status_code == 200
    assert response.json()['genre'] == 'm'
    assert response.json()['document_id'] == 1

def test_update(client: TestClient):
    assert client.post('/customers/', json={
        'first_name': 'PRIMEIRO',
        'last_name': 'ULTIMO',
        'phone_number': '999999999',
        'genre': 'm',
        'document_id': 1,
        'birth_date':'2021-12-15',
        'user':{
            'display_name': 'DISPLAY',
            'email':'email@email.com',
            'password': '123',
            'role': 'user'
        }
    }).status_code == 201
    assert client.put('/customers/1',json={
        'first_name': 'ULTIMO',
        'last_name': 'PRIMEIRO',
        'phone_number': '999999999',
        'genre': 'm',
        'birth_date':'2000-12-15'
    }).status_code == 200
    response = client.get('/customers/1')
    assert response.json() == {
        "first_name": "ULTIMO",
        "last_name": "PRIMEIRO",
        "phone_number": "999999999",
        "genre": "m",
        "document_id": 1,
        "birth_date": "2000-12-15",
        "id": 1
    }
    
    