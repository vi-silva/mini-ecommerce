from fastapi.testclient import TestClient

def test_create(client: TestClient, admin_auth_header):
    response = client.post('/coupons/', headers=admin_auth_header, json={
        'code':'TESTE',
        'expire_at':'2022-12-12T12:12:12.121000',
        'limit':12,
        'type':'value',
        'value':12
    })
    assert response.status_code == 201
    response = client.get('/coupons/1', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['code'] == 'TESTE'
    assert response.json()['expire_at'] == '2022-12-12T12:12:12.121000'
    assert response.json()['limit'] == 12
    assert response.json()['type'] == 'value'
    assert response.json()['value'] == 12

def test_update(client:TestClient, admin_auth_header):
    client.post('/coupons/', headers=admin_auth_header, json={
        'code':'TESTE',
        'expire_at':'2022-12-12T12:12:12.121000',
        'limit':12,
        'type':'value',
        'value':12
    })
    assert client.put('/coupons/1', headers=admin_auth_header, json={
        'limit':13,
        'expire_at': '2023-12-12T12:12:12.121000'
    }).status_code == 200
    response = client.get('/coupons/1', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['code'] == 'TESTE'
    assert response.json()['expire_at'] == '2023-12-12T12:12:12.121000'
    assert response.json()['limit'] == 13
    assert response.json()['type'] == 'value'
    assert response.json()['value'] == 12

def test_get_all(client: TestClient, admin_auth_header):
    for i in range(1,10):
        client.post('/coupons/', headers=admin_auth_header, json={
            'code':f'TESTE {i}',
            'expire_at':'2022-12-12T12:12:12.121000',
            'limit':i,
            'type':'value',
            'value':i
        })
    response = client.get('/coupons/',headers=admin_auth_header)
    assert response.status_code == 200
    for i in range(9):
        assert response.json()[i]['code'] == f'TESTE {i+1}'
        assert response.json()[i]['expire_at'] == '2022-12-12T12:12:12.121000'
        assert response.json()[i]['limit'] == i+1
        assert response.json()[i]['type'] == 'value'
        assert response.json()[i]['value'] == i+1

def test_delete(client: TestClient, admin_auth_header):
    client.post('/coupons/', headers=admin_auth_header, json={
        'code':'TESTE',
        'expire_at':'2022-12-12T12:12:12.121000',
        'limit':12,
        'type':'value',
        'value':12
    })
    response = client.delete('/coupons/1',headers = admin_auth_header)
    assert response.status_code == 200
    assert response.json() == None

def test_create_repeated_code(client: TestClient, admin_auth_header):
    response = client.post('/coupons/', headers=admin_auth_header, json={
        'code':'TESTE',
        'expire_at':'2022-12-12T12:12:12.121000',
        'limit':12,
        'type':'value',
        'value':12
    })
    assert response.status_code == 201
    response = client.post('/coupons/', headers=admin_auth_header, json={
        'code':'TESTE',
        'expire_at':'2022-12-12T12:12:12.121000',
        'limit':12,
        'type':'value',
        'value':12
    })
    assert response.status_code == 403
    assert response.json()['detail'] == 'Invalid Coupon'

def test_update(client: TestClient, admin_auth_header):
    response = client.post('/coupons/', headers=admin_auth_header, json={
        'code':'TESTE',
        'expire_at':'2022-12-12T12:12:12.121000',
        'limit':12,
        'type':'value',
        'value':12
    })
    assert response.status_code == 201
    response = client.put('/coupons/1', headers=admin_auth_header, json={
        'code':'ATT',
        'expire_at':'2023-12-12T12:12:12.121000',
        'limit':13,
        'type':'percentage',
        'value':120
    })
    assert response.status_code == 200
    response = client.get('/coupons/1',headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['code'] == 'TESTE'
    assert response.json()['expire_at'] == '2023-12-12T12:12:12.121000'
    assert response.json()['limit'] == 13
    assert response.json()['type'] == 'value'
    assert response.json()['value'] == 12
