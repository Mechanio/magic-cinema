def test_delete_actor(client, app, authentication_headers):
    response = client.delete('/actors/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_ticket(client, app, authentication_headers):
    response = client.delete('/tickets/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_movie_session(client, app, authentication_headers):
    response = client.delete('/sessions/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_auditorium(client, app, authentication_headers):
    response = client.delete('/auditorium/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_director(client, app, authentication_headers):
    response = client.delete('/director/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_genre(client, app, authentication_headers):
    response = client.delete('/genres/1', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


def test_delete_user(client, app, authentication_headers):
    response = client.delete('/users/2', headers=authentication_headers(is_admin=True))
    assert response.json['message'] == "Deleted"


# def test_delete_movie(client, app, authentication_headers):
#     response = client.delete('/movies/1', headers=authentication_headers(is_admin=True))
#     assert response.json['message'] == "Deleted"
