def test_create_movie(client, app, authentication_headers):
    response = client.post('/movies', json={
        "name": "Annette",
        "description": "About Annette",
        "director_id": 1,
        "year": 2021,
        "month": 6,
        "day": 6,
        "genres": ["musical"],
        "actors": ["Adam Driver"],
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_movie(client, app, authentication_headers):
    response = client.patch('/movies/1', json={
        "month": 7,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_delete_genre_movie(client, app, authentication_headers):
    response = client.patch('/movies/changes/1', json={
        "genres": ["musical"],
    }, headers=authentication_headers(is_admin=True))
    assert response.json["musical"] == "Deleted"


def test_get_movie(client, app):
    response = client.get('/movies/1')
    assert response.json['name'] == "Annette" and response.json['description'] == "About Annette"


def test_get_movies(client, app):
    response = client.get('/movies/')
    assert response.json[0]['name'] == "Annette" and response.json[0]['description'] == "About Annette"
