import pytest
from API.api import app
from Database.db_connection import connect_db
@pytest.fixture()
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
     yield client
@pytest.fixture()
def clean_db():
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("DELETE FROM hardware_store")
    connect.commit()
    connect.close()
def test_id(client):
    response = client.get('/store/1')
    assert response.status_code == 200
    if response.status_code != 200:
        assert response.status_code == 404
def test_update_row(client,clean_db):
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("INSERT INTO hardware_store(Customer, Products, Price) VALUES (%s, %s, %s)",
                   ("Gabriel",'Chainsaw',120.00))
    connect.commit()
    item_id = cursor.lastrowid
    connect.close()
    data={'Customer':'Gabriel','Products':'Chainsaw','Price':120.00}
    response = client.put(f'/store/{item_id}',json=data)
    assert response.status_code == 200
    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hardware_store WHERE id=%s", (item_id,))
    row=cursor.fetchone()
    connect.close()
    assert row['Customer'] == 'Gabriel'
    assert row['Products'] == 'Chainsaw'
    assert row['Price'] == 120.00

def test_post_new_row(client,clean_db):
    data = {'Customer': 'Gabriel', 'Products': 'Chainsaw', 'Price': 120.00}
    response = client.post(f'/store', json=data)
    assert response.status_code == 201

    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hardware_store WHERE Customer=%s AND Products=%s AND Price=%s",
    ("Gabriel","Chainsaw",120.00))
    row = cursor.fetchone()
    connect.close()
    assert row['Customer'] == 'Gabriel'
    assert row['Products'] == 'Chainsaw'
    assert row['Price'] == 120.00
def test_delete_row(client,clean_db):
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute("INSERT INTO hardware_store(Customer, Products, Price) VALUES (%s, %s, %s)",
                   ("Gabriel", 'Chainsaw', 120.00))
    connect.commit()
    item_id = cursor.lastrowid
    connect.close()
    response = client.delete(f'/store/{item_id}')
    assert response.status_code == 200
    connect = connect_db()
    cursor = connect.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hardware_store WHERE id=%s", (item_id,))
    result = cursor.fetchone()
    connect.close()
    assert result is None




