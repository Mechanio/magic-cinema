def test_create_movie_session(client, app, authentication_headers):
    response = client.post('/api/sessions/', json={
        "movie_id": 1,
        "auditorium_id": 1,
        "director_id": 1,
        "year": 2021,
        "month": 6,
        "day": 6,
        "hour": 12,
        "minute": 15,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["id"] == 1


def test_update_movie_session(client, app, authentication_headers):
    response = client.patch('/api/sessions/1', json={
        "month": 7,
    }, headers=authentication_headers(is_admin=True))
    assert response.json["message"] == "Updated"


def test_get_movie_session(client, app):
    response = client.get('/api/sessions/1')
    assert response.json['movie_id'] == 1


def test_get_movies_sessions(client, app):
    response = client.get('/api/sessions/')
    assert response.json[0]['movie_id'] == 1
