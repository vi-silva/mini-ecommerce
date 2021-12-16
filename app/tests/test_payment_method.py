from fastapi.testclient import TestClient

def test_create(client: TestClient, admin_auth_header):
    response = client.post('/payment-method/', headers=admin_auth_header,json={
        'name': 'TEST METHOD',
        'enabled': True
    })
    assert response.status_code == 201
    response = client.get('/payment-method/1', headers= admin_auth_header)
    assert response.status_code == 200
    assert response.json()['name'] == 'TEST METHOD'
    assert response.json()['enabled'] == True

def test_show(client: TestClient, admin_auth_header):
    for i in range(1,4):
        client.post('/payment-method/', headers=admin_auth_header,json={
            'name': f'TEST METHOD {i}',
            'enabled': True
        })
    for i in range(1,4):
        response = client.get(f'/payment-method/{i}', headers= admin_auth_header)
        assert response.status_code == 200
        assert response.json()['name'] == f'TEST METHOD {i}'
        assert response.json()['enabled'] == True

def test_get_all(client: TestClient, admin_auth_header):
    for i in range(1,10):
        client.post('/payment-method/', headers=admin_auth_header,json={
            'name': f'TEST METHOD {i}',
            'enabled': True
        })
    response = client.get('/payment-method/', headers= admin_auth_header)
    assert response.status_code == 200
    for i in range(9):
        assert response.json()[i]['name'] == f'TEST METHOD {i+1}'
        assert response.json()[i]['enabled'] == True

def test_update(client: TestClient, admin_auth_header):
    for i in range(1,10):
        client.post('/payment-method/', headers=admin_auth_header,json={
            'name': f'TEST METHOD {i}',
            'enabled': True
        })
        client.put('/payment-method/'+str(i), headers=admin_auth_header, json={
            'name': f'TEST METHOD {i}',
            'enabled': False
        })
    response = client.get('/payment-method/', headers= admin_auth_header)
    assert response.status_code == 200
    for i in range(9):
        assert response.json()[i]['name'] == f'TEST METHOD {i+1}'
        assert response.json()[i]['enabled'] == False
    
def test_get_all(client: TestClient, admin_auth_header):
    for i in range(1,10):
        client.post('/payment-method/', headers=admin_auth_header,json={
            'name': f'TEST METHOD {i}',
            'enabled': True
        })
    response = client.get('/payment-method/', headers= admin_auth_header)
    assert response.status_code == 200
    for i in range(9):
        assert response.json()[i]['name'] == f'TEST METHOD {i+1}'
        assert response.json()[i]['enabled'] == True

def test_delete(client: TestClient, admin_auth_header):
    response = client.post('/payment-method/', headers=admin_auth_header,json={
        'name': 'TEST METHOD',
        'enabled': True
    })
    assert response.status_code == 201
    response = client.delete('/payment-method/', headers=admin_auth_header)
    assert response.status_code == 405
    response = client.get('/payment-method/1',headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['name'] == 'TEST METHOD'
    assert response.json()['enabled'] == True