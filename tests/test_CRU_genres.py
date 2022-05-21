def test_create_genre(client, app, authentication_headers):
    response = client.post('/genres', json={
        "genre": "music",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_genre(client, app, authentication_headers):
    response = client.patch('/genres/1', json={
        "genre": "musical",
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_genre(client, app):
    response = client.get('/genres/1')
    assert response.json['genre'] == "musical"


def test_get_auditoriums(client, app):
    response = client.get('/genres/')
    assert response.json[0]['genre'] == "musical"
