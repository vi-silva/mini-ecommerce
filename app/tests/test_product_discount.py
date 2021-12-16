from fastapi.testclient import TestClient

def test_create(client: TestClient, admin_auth_header, product_factory, payment_method_factory):
    product = product_factory()
    payment_method = payment_method_factory()
    response = client.post('/product-discount/',headers=admin_auth_header, json={
        'mode': 'value',
        'value': 2.50,
        'payment_method_id': payment_method.id,
        'product_id': product.id
    })
    assert response.status_code == 201
    response = client.get('/product-discount/1', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['mode'] == 'value'
    assert response.json()['payment_method_id'] == payment_method.id
    assert response.json()['product_id'] == product.id

def test_show(client: TestClient, admin_auth_header, product_factory, payment_method_factory):
    for i in range(1,4):
        product = product_factory()
        payment_method = payment_method_factory()
        client.post('/product-discount/',headers=admin_auth_header, json={
            'mode': 'value',
            'value': i,
            'payment_method_id': payment_method.id,
            'product_id': product.id
        })
    for i in range(1,4):
        response = client.get(f'/product-discount/{i}', headers=admin_auth_header)
        assert response.status_code == 200
        assert response.json()['mode'] == 'value'
        assert response.json()['value'] == i
    
def test_get_all(client: TestClient, admin_auth_header, product_factory, payment_method_factory):
    for i in range(1,10):
        product = product_factory()
        payment_method = payment_method_factory()
        client.post('/product-discount/',headers=admin_auth_header, json={
            'mode': 'value',
            'value': i,
            'payment_method_id': payment_method.id,
            'product_id': product.id
        })
    response = client.get('/product-discount/', headers=admin_auth_header)
    assert response.status_code == 200
    for i in range(9):
        assert response.json()[i]['mode'] == 'value'
        assert response.json()[i]['value'] == i+1
    
def test_update(client: TestClient, admin_auth_header, product_factory, payment_method_factory):
    for i in range(1,10):
        product = product_factory()
        payment_method = payment_method_factory()
        client.post('/product-discount/',headers=admin_auth_header, json={
            'mode': 'value',
            'value': i,
            'payment_method_id': payment_method.id,
            'product_id': product.id
        })
        client.put(f'/product-discount/{i}', headers=admin_auth_header, json={
            'mode':'percentage',
            'value':i+1,
            'payment_method_id': payment_method.id,
            'product_id': product.id
        })
    for i in range(1,10):
        response = client.get(f'/product-discount/{i}', headers=admin_auth_header)
        assert response.status_code == 200
        assert response.json()['mode'] == 'percentage'
        assert response.json()['value'] == i+1

def test_delete(client: TestClient, admin_auth_header, product_factory, payment_method_factory):
    product = product_factory()
    payment_method = payment_method_factory()
    response = client.post('/product-discount/',headers=admin_auth_header, json={
        'mode': 'value',
        'value': 2.50,
        'payment_method_id': payment_method.id,
        'product_id': product.id
    })
    assert response.status_code == 201
    response = client.delete('/product-discount/1', headers=admin_auth_header)
    assert response.status_code == 200
    response = client.get('/product-discount/1', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json() == None

def test_product_discount_disabled_payment(client: TestClient, admin_auth_header, product_factory, disabled_payment_method_factory):
    product = product_factory()
    payment_method = disabled_payment_method_factory()
    response = client.post('/product-discount/',headers=admin_auth_header, json={
        'mode': 'value',
        'value': 2.50,
        'payment_method_id': payment_method.id,
        'product_id': product.id
    })
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid payment method'

def test_multiple_discount_same_payment_method(client: TestClient, admin_auth_header, product_factory, payment_method_factory):
    product = product_factory()
    payment_method = payment_method_factory()
    response = client.post('/product-discount/',headers=admin_auth_header, json={
        'mode': 'value',
        'value': 2.50,
        'payment_method_id': payment_method.id,
        'product_id': product.id
    })
    assert response.status_code == 201
    response = client.post('/product-discount/',headers=admin_auth_header, json={
        'mode': 'value',
        'value': 2.50,
        'payment_method_id': payment_method.id,
        'product_id': product.id
    })
    assert response.status_code == 403
    assert response.json()['detail'] == 'Payment method already discounted for this product'
    