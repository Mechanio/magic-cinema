def test_create_director(client, app, authentication_headers):
    response = client.post('/director', json={
        "firstname": "Leos",
        "lastname": "Corox",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_director(client, app, authentication_headers):
    response = client.patch('/director/1', json={
        "firstname": "Leos",
        "lastname": "Carax",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_director(client, app):
    response = client.get('/director/1')
    assert response.json['firstname'] == "Leos" and response.json['lastname'] == "Carax"


def test_get_directors(client, app):
    response = client.get('/director/')
    assert response.json[0]['firstname'] == "Leos" and response.json[0]['lastname'] == "Carax"
