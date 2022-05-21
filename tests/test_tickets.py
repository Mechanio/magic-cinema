def test_create_ticket(client, app, authentication_headers):
    response = client.post('/tickets', json={
        "session_id": 1,
        "user_id": 1,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_ticket(client, app, authentication_headers):
    response = client.patch('/tickets/1', json={
        "user_id": 2,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_ticket(client, app, authentication_headers):
    response = client.get('/tickets/1', headers=authentication_headers(is_admin=True))
    assert response.json['user_id'] == 2 and response.json['session_id'] == 1


def test_get_tickets(client, app, authentication_headers):
    response = client.get('/tickets/', headers=authentication_headers(is_admin=True))
    assert response.json[0]['user_id'] == 2 and response.json[0]['session_id'] == 1
