from fastapi.testclient import TestClient


def test_product_create(client: TestClient, category_factory, supplier_factory, admin_auth_header):
    category = category_factory()
    supplier = supplier_factory()

    client.post('/product/', headers=admin_auth_header,
                           json={
                               'description': 'descricao',
                               'price': 100,
                               'image': 'image.dev',
                               'technical_details': 'bla bla',
                               'visible': True,
                               'category_id': category.id,
                               'supplier_id': supplier.id
                           })
    response = client.get('/product/1', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['description'] == 'descricao'
    assert response.json()['category_id'] == category.id
    assert response.json()['supplier_id'] == supplier.id

def test_product_show(client: TestClient, category_factory, supplier_factory, admin_auth_header):
    category = category_factory()
    supplier = supplier_factory()
    for i in range(1,4):
        client.post('/product/', headers=admin_auth_header,
                            json={
                                'description': f'descricao {i-1}',
                                'price': 100,
                                'image': 'image.dev',
                                'technical_details': f'bla bla {i-1}',
                                'visible': True,
                                'category_id': category.id,
                                'supplier_id': supplier.id
                            })
    for i in range(1,4):
        response = client.get(f'/product/{i}', headers=admin_auth_header)
        assert response.status_code == 200
        assert response.json()['description'] == f'descricao {i-1}'
        assert response.json()['technical_details'] == f'bla bla {i-1}'
        assert response.json()['category_id'] == category.id
        assert response.json()['supplier_id'] == supplier.id

def test_product_get_all(client: TestClient, category_factory, supplier_factory, admin_auth_header):
    category = category_factory()
    supplier = supplier_factory()
    for i in range(1,10):
        client.post('/product/', headers=admin_auth_header,
                            json={
                                'description': f'descricao {i-1}',
                                'price': 100,
                                'image': 'image.dev',
                                'technical_details': f'bla bla {i-1}',
                                'visible': True,
                                'category_id': category.id,
                                'supplier_id': supplier.id
                            })
    response = client.get('/product/', headers=admin_auth_header)
    assert response.status_code == 200
    for i in range(9):
        assert response.json()[i]['description'] == f'descricao {i}'
        assert response.json()[i]['technical_details'] == f'bla bla {i}'
        assert response.json()[i]['category_id'] == category.id
        assert response.json()[i]['supplier_id'] == supplier.id
