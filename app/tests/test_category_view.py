from fastapi.testclient import TestClient

def test_category_create(client: TestClient,admin_auth_header):
    response = client.post('/category/',headers=admin_auth_header, json={
        'name': 'Categoria 1'
    })

    assert response.status_code == 201
    assert response.json()['id'] == 1


def test_category_update(client: TestClient, admin_auth_header):
    response = client.post('/category/',
     headers=admin_auth_header,
     json={
        'name': 'Categoria 1'
    })
    assert response.status_code == 201

    response = client.put(
        '/category/1',headers=admin_auth_header, json={'name': 'Categoria alterada'})

    assert response.status_code == 200
    # assert response.json()['name'] == 'Categoria alterada' #COMENTADO POIS ENDPOINT NAO POSSUI ESSE RETORNO

def test_category_show(client: TestClient, admin_auth_header):
    response = client.post('/category/',headers=admin_auth_header, json={
        'name': 'Categoria 1'
    })
    assert response.status_code == 201
    response = client.get('/category/1',headers=admin_auth_header)
    assert response.json()['name'] == 'Categoria 1'

def test_category_get_all(client: TestClient, admin_auth_header,):
    response = client.post('/category/',headers=admin_auth_header, json={
        'name': 'Categoria 1'
    })
    assert response.status_code == 201
    response = client.post('/category/',headers=admin_auth_header, json={
        'name': 'Categoria 2'
    })
    assert response.status_code == 201
    response = client.get('/category/',headers=admin_auth_header)
    assert response.json()[0]['name'] == 'Categoria 1'
    assert response.json()[1]['name'] == 'Categoria 2'