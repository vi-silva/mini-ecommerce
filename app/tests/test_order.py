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
    