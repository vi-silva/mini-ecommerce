from fastapi.testclient import TestClient
from app.services.auth_service import get_user

def test_create(client: TestClient, address_factory, product_factory, payment_method_factory, user_customer_data, admin_auth_header):
    customer_auth_header, customer = user_customer_data
    address = address_factory(customer_id = customer.id)
    product = product_factory()
    payment_method = payment_method_factory()
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
    assert response.json()['customer_id'] == customer.id
    assert response.json()['customer'] == {
      "first_name": customer.first_name,
      "last_name": customer.last_name,
      "phone_number": customer.phone_number,
      "genre": customer.genre,
      "document_id": int(customer.document_id), #retorna como str por isso a conversao
      "birth_date": str(customer.birth_date), #retorna como objeto por isso a conversao
      "id": customer.id,
    }
    assert response.json()['address_id'] == address.id
    assert response.json()['address'] == {
      "address": address.address,
      "city": address.city,
      "state": address.state,
      "number": address.number,
      "zipcode": address.zipcode,
      "neighbourhood": address.neighbourhood,
      "primary": address.primary,
      "customer_id": int(address.customer_id),
      "id": int(address.id),
      "customer":{
        "first_name": address.customer.first_name,
        "last_name": address.customer.last_name,
        "phone_number": address.customer.phone_number,
        "genre": address.customer.genre,
        "document_id": int(address.customer.document_id),
        "birth_date": str(address.customer.birth_date),
        "id": int(address.customer.id)
      }
    }
    assert response.json()['total_value'] == round(float(product.price * 13),2)
    assert response.json()['payment_form_id'] == int(payment_method.id)
    assert response.json()['payment_form'] == {
        "name" : payment_method.name,
        "enabled" : payment_method.enabled,
        "id" : int(payment_method.id)
    }
    
    
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

def test_value_coupon_order(client: TestClient, product_factory, payment_method_factory, user_customer_data, admin_auth_header, address_factory, coupon_factory):
    customer_auth_header, customer = user_customer_data
    address = address_factory(customer_id = customer.id)
    product = product_factory()
    payment_method = payment_method_factory()
    coupon = coupon_factory(limit=1)
    assert client.post('/orders/', headers=customer_auth_header, json={
        'address_id': address.id,
        'payment_form_id': payment_method.id,
        'coupon_code': coupon.code,
        'products':[ 
            {
                'id': product.id,
                'quantity':13
            }
        ]
    }).status_code == 201
    response = client.get('/orders/1',headers = admin_auth_header)
    assert response.status_code == 200
    assert response.json() == {
        'number': response.json()['number'], #numero aleatório
        'status': 'order_placed', 
        'customer_id': int(customer.id), 
        'customer': {
            'first_name': customer.first_name, 
            'last_name': customer.last_name, 
            'phone_number': customer.phone_number, 
            'genre': customer.genre, 
            'document_id': int(customer.document_id), 
            'birth_date': str(customer.birth_date), 
            'id': int(customer.id)
        }, 
        'created_at': response.json()['created_at'], #timedate do momento que foi criado
        'address_id': int(address.id), 
        'address': {
            "address": address.address,
            "city": address.city,
            "state": address.state,
            "number": address.number,
            "zipcode": address.zipcode,
            "neighbourhood": address.neighbourhood,
            "primary": address.primary,
            "customer_id": int(address.customer_id),
            "id": int(address.id),
            "customer":{
                "first_name": address.customer.first_name,
                "last_name": address.customer.last_name,
                "phone_number": address.customer.phone_number,
                "genre": address.customer.genre,
                "document_id": int(address.customer.document_id),
                "birth_date": str(address.customer.birth_date),
                "id": int(address.customer.id)
            }
        },
        'total_value': round(float(product.price * 13),2), 
        'payment_form_id': int(payment_method.id), 
        'payment_form': {
            'name': payment_method.name, 
            'enabled': payment_method.enabled, 
            'id': int(payment_method.id)
        }, 
        'total_discount': int(coupon.value)
    }
    
def test_update(client: TestClient, address_factory, product_factory, payment_method_factory, user_customer_data, admin_auth_header):
    customer_auth_header, customer = user_customer_data
    address = address_factory(customer_id = customer.id)
    product = product_factory()
    payment_method = payment_method_factory()
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
    assert client.patch('/orders/1?order_status=order_paid', headers=admin_auth_header).status_code == 200
    response = client.get('/orders/1',headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['status'] == 'order_paid'
    assert client.patch('/orders/1?order_status=order_cancelled', headers=admin_auth_header).status_code == 200
    response = client.get('/orders/1',headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()['status'] == 'order_cancelled'
    
