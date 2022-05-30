def test_delete_actor(client, app, authentication_headers):
    response = client.delete('/api/actors/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_ticket(client, app, authentication_headers):
    response = client.delete('/api/tickets/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_movie_session(client, app, authentication_headers):
    response = client.delete('/api/sessions/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_auditorium(client, app, authentication_headers):
    response = client.delete('/api/auditorium/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_director(client, app, authentication_headers):
    response = client.delete('/api/director/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_genre(client, app, authentication_headers):
    response = client.delete('/api/genres/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_user(client, app, authentication_headers):
    response = client.delete('/api/users/2', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


# def test_delete_movie(client, app, authentication_headers):
#     response = client.delete('/api/movies/1', headers=authentication_headers(is_admin=True))
#     assert response.json['message'] == "Deleted"
