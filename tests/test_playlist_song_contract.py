from fastapi.testclient import TestClient


def create_song(client: TestClient, *, title: str) -> dict:
    response = client.post(
        "/songs/",
        json={
            "title": title,
            "artist": "Relationship Artist",
            "duration_seconds": 180,
        },
    )
    assert response.status_code == 201
    return response.json()


def create_playlist(client: TestClient, *, name: str) -> dict:
    response = client.post("/playlists/", json={"name": name})
    assert response.status_code == 201
    return response.json()


def test_playlist_song_link_adds_song_to_playlist(client: TestClient) -> None:
    song = create_song(client, title="Linked Song")
    playlist = create_playlist(client, name="Link Contract")

    add_response = client.post(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert add_response.status_code == 201

    added_song_ids = [item["id"] for item in add_response.json()["songs"]]
    assert added_song_ids == [song["id"]]


def test_playlist_song_duplicate_link_does_not_duplicate_relation(client: TestClient) -> None:
    song = create_song(client, title="Linked Song")
    playlist = create_playlist(client, name="Link Contract")

    first_add_response = client.post(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert first_add_response.status_code == 201

    add_again_response = client.post(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert add_again_response.status_code == 201

    second_add_song_ids = [item["id"] for item in add_again_response.json()["songs"]]
    assert second_add_song_ids.count(song["id"]) == 1


def test_playlist_song_unlink_removes_relation(client: TestClient) -> None:
    song = create_song(client, title="Linked Song")
    playlist = create_playlist(client, name="Link Contract")

    add_response = client.post(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert add_response.status_code == 201

    remove_response = client.delete(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert remove_response.status_code == 204

    playlist_after_remove = client.get(f"/playlists/{playlist['id']}")
    assert playlist_after_remove.status_code == 200
    assert playlist_after_remove.json()["songs"] == []


def test_playlist_song_repeated_unlink_is_idempotent(client: TestClient) -> None:
    song = create_song(client, title="Linked Song")
    playlist = create_playlist(client, name="Link Contract")

    add_response = client.post(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert add_response.status_code == 201

    remove_response = client.delete(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert remove_response.status_code == 204

    remove_again_response = client.delete(f"/playlists/{playlist['id']}/songs/{song['id']}")
    assert remove_again_response.status_code == 204


def test_playlist_song_relation_missing_resources_return_404(client: TestClient) -> None:
    song = create_song(client, title="Existing Song")
    playlist = create_playlist(client, name="Existing Playlist")

    missing_playlist_add_response = client.post(f"/playlists/99999/songs/{song['id']}")
    assert missing_playlist_add_response.status_code == 404
    assert missing_playlist_add_response.json() == {"detail": "Playlist not found"}

    missing_song_add_response = client.post(f"/playlists/{playlist['id']}/songs/99999")
    assert missing_song_add_response.status_code == 404
    assert missing_song_add_response.json() == {"detail": "Song not found"}

    missing_playlist_remove_response = client.delete(f"/playlists/99999/songs/{song['id']}")
    assert missing_playlist_remove_response.status_code == 404
    assert missing_playlist_remove_response.json() == {"detail": "Playlist not found"}

    missing_song_remove_response = client.delete(f"/playlists/{playlist['id']}/songs/99999")
    assert missing_song_remove_response.status_code == 404
    assert missing_song_remove_response.json() == {"detail": "Song not found"}


def test_playlist_song_ids_patch_replaces_and_deduplicates_links(client: TestClient) -> None:
    first_song = create_song(client, title="First")
    second_song = create_song(client, title="Second")

    playlist_response = client.post(
        "/playlists/",
        json={
            "name": "Replace Links",
            "song_ids": [first_song["id"]],
        },
    )
    assert playlist_response.status_code == 201
    playlist_id = playlist_response.json()["id"]

    replace_response = client.patch(
        f"/playlists/{playlist_id}",
        json={"song_ids": [second_song["id"], second_song["id"]]},
    )
    assert replace_response.status_code == 200
    song_ids = [song["id"] for song in replace_response.json()["songs"]]
    assert song_ids == [second_song["id"]]


def test_playlist_song_relation_rejects_invalid_identifier_types(client: TestClient) -> None:
    invalid_playlist_id_response = client.post("/playlists/invalid/songs/1")
    assert invalid_playlist_id_response.status_code == 422

    invalid_song_id_response = client.post("/playlists/1/songs/invalid")
    assert invalid_song_id_response.status_code == 422
