from fastapi.testclient import TestClient
from app.services.auth_service import get_user

def test_create(client: TestClient, address_factory, product_factory, payment_method_factory, user_customer_data, admin_auth_header):
    customer_auth_header, customer = user_customer_data
    address = address_factory(customer_id = customer.id)
    product = product_factory()
    payment_method = payment_method_factory()
    #se chamar o auth header voce cria um novo usuario e gera erro de usuario invalido no pedido
    assert client.post('/orders/', headers=customer_auth_header, json={
        'address_id': address.id,
        'payment_form_id': payment_method.id,
        'coupon_code': 'TESTE',
        'products':[ 
            {
                'id': product.id,
                'quantity':13
            }
        ]
    }).status_code == 201
    response = client.get('/orders/1', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['status'] == 'order_placed'
    
def test_create_order_admin(client: TestClient, address_factory, product_factory, payment_method_factory, user_customer_data, admin_auth_header):
    customer_auth_header, customer = user_customer_data
    address = address_factory(customer_id = customer.id)
    product = product_factory()
    payment_method = payment_method_factory()
    #se chamar o auth header voce cria um novo usuario e gera erro de usuario invalido no pedido
    response = client.post('/orders/', headers=admin_auth_header, json={
        'address_id': address.id,
        'payment_form_id': payment_method.id,
        'coupon_code': 'TESTE',
        'products':[ 
            {
                'id': product.id,
                'quantity':13
            }
        ]
    })
    assert response.status_code == 404
    assert response.json()['detail'] == 'Invalid user'

def test_create_order_invalid_address(client: TestClient, product_factory, payment_method_factory, user_customer_data, admin_auth_header, address_factory):
    customer_auth_header, customer = user_customer_data
    address = address_factory(customer_id = 0)
    product = product_factory()
    payment_method = payment_method_factory()
    #se chamar o auth header voce cria um novo usuario e gera erro de usuario invalido no pedido
    response = client.post('/orders/', headers=customer_auth_header, json={
        'address_id': address.id,
        'payment_form_id': payment_method.id,
        'coupon_code': 'TESTE',
        'products':[ 
            {
                'id': product.id,
                'quantity':13
            }
        ]
    })
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid address'
    response = client.post('/orders/', headers=customer_auth_header, json={
        'address_id': 0,
        'payment_form_id': payment_method.id,
        'coupon_code': 'TESTE',
        'products':[ 
            {
                'id': product.id,
                'quantity':13
            }
        ]
    })
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid address'

def test_create_order_invalid_products(client: TestClient, product_factory, payment_method_factory, user_customer_data, admin_auth_header, address_factory):
    customer_auth_header, customer = user_customer_data
    address = address_factory(customer_id = customer.id)
    product = product_factory()
    payment_method = payment_method_factory()
    #se chamar o auth header voce cria um novo usuario e gera erro de usuario invalido no pedido
    response = client.post('/orders/', headers=customer_auth_header, json={
        'address_id': address.id,
        'payment_form_id': payment_method.id,
        'coupon_code': 'TESTE',
        'products':[ 
            {
                'id': product.id,
                'quantity':13
            },
            {
                'id': 0,
                'quantity':14
            }
        ]
    })
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid product'
