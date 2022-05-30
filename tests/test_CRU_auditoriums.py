def test_create_auditorium(client, app, authentication_headers):
    response = client.post('/api/auditorium/', json={
        "seats": 25,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_auditorium(client, app, authentication_headers):
    response = client.patch('/api/auditorium/1', json={
        "seats": 20,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_auditorium(client, app):
    response = client.get('/api/auditorium/1')
    assert response.json['seats'] == 20


def test_get_auditoriums(client, app):
    response = client.get('/api/auditorium/')
    assert response.json[0]['seats'] == 20
