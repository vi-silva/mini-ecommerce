from fastapi.testclient import TestClient

def test_create(client: TestClient,admin_auth_header):
    response = client.post('/supplier/',headers=admin_auth_header,json={
        'name' : 'VENDEDOR 1'
    })
    assert response.status_code == 201

def test_update(client: TestClient, admin_auth_header):
    client.post('/supplier/',headers=admin_auth_header,json={
        'name' : 'VENDEDOR 1'
    })
    client.put('/supplier/1',headers=admin_auth_header,json={
        'name' : 'NOME ATUALIZADO'
    })
    response = client.get('/supplier/1',headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['name'] == 'NOME ATUALIZADO'

def test_show(client: TestClient, admin_auth_header):
    for i in range(1,4):
        client.post('/supplier/',headers=admin_auth_header,json={
            'name' : f'VENDEDOR {i}'
        })
    for i in range(1,4):
        response = client.get(f'/supplier/{i}',headers=admin_auth_header)
        assert response.status_code == 200
        assert response.json()['name'] == f'VENDEDOR {i}'

def test_get_all(client: TestClient, admin_auth_header):
    for i in range(1,7):
        client.post('/supplier/',headers=admin_auth_header,json={
            'name' : f'VENDEDOR {i}'
        })
    response = client.get('/supplier/', headers=admin_auth_header)
    assert response.status_code == 200
    for i in range(1,7):
        assert response.json()[i-1]['name'] == f'VENDEDOR {i}'

def test_delete(client: TestClient, admin_auth_header):
    response = client.post('/supplier/',headers=admin_auth_header,json={
        'name' : 'VENDEDOR 1'
    })
    assert response.status_code == 201
    response = client.delete('/supplier/1', headers=admin_auth_header)
    assert response.status_code == 405
    response = client.get('/supplier/1', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['name'] == 'VENDEDOR 1'