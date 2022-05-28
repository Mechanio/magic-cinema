def test_create_actor(client, app, authentication_headers):
    response = client.post('/api/actors/', json={
        "firstname": "Adam",
        "lastname": "Drover",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_actor(client, app, authentication_headers):
    response = client.patch('/api/actors/1', json={
        "firstname": "Adam",
        "lastname": "Driver",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_actor(client, app):
    response = client.get('/api/actors/1')
    assert response.json['firstname'] == "Adam" and response.json['lastname'] == "Driver"


def test_get_actors(client, app):
    response = client.get('/api/actors/')
    assert response.json[0]['firstname'] == "Adam" and response.json[0]['lastname'] == "Driver"
