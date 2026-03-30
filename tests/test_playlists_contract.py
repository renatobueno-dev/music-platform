from fastapi.testclient import TestClient


def test_playlists_crud_contract(client: TestClient) -> None:
    create_response = client.post(
        "/playlists/",
        json={
            "name": "Daily Mix",
            "description": "Work playlist",
            "is_public": True,
        },
    )
    assert create_response.status_code == 201
    created_playlist = create_response.json()
    playlist_id = created_playlist["id"]
    assert created_playlist["name"] == "Daily Mix"
    assert created_playlist["description"] == "Work playlist"
    assert created_playlist["is_public"] is True
    assert created_playlist["songs"] == []

    list_response = client.get("/playlists/")
    assert list_response.status_code == 200
    listed_playlists = list_response.json()
    assert any(playlist["id"] == playlist_id for playlist in listed_playlists)

    read_response = client.get(f"/playlists/{playlist_id}")
    assert read_response.status_code == 200
    read_playlist = read_response.json()
    assert read_playlist["id"] == playlist_id
    assert read_playlist["name"] == "Daily Mix"
    assert read_playlist["description"] == "Work playlist"
    assert read_playlist["is_public"] is True
    assert read_playlist["songs"] == []

    patch_response = client.patch(
        f"/playlists/{playlist_id}",
        json={
            "description": "Updated description",
            "is_public": False,
        },
    )
    assert patch_response.status_code == 200
    patched_playlist = patch_response.json()
    assert patched_playlist["description"] == "Updated description"
    assert patched_playlist["is_public"] is False
    assert patched_playlist["name"] == "Daily Mix"
    assert patched_playlist["songs"] == []

    delete_response = client.delete(f"/playlists/{playlist_id}")
    assert delete_response.status_code == 204

    read_deleted_response = client.get(f"/playlists/{playlist_id}")
    assert read_deleted_response.status_code == 404
    assert read_deleted_response.json() == {"detail": "Playlist not found"}


def test_playlist_missing_id_returns_404_for_get_patch_and_delete(client: TestClient) -> None:
    missing_playlist_id = 99999

    get_response = client.get(f"/playlists/{missing_playlist_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Playlist not found"}

    patch_response = client.patch(
        f"/playlists/{missing_playlist_id}",
        json={"description": "Any description"},
    )
    assert patch_response.status_code == 404
    assert patch_response.json() == {"detail": "Playlist not found"}

    delete_response = client.delete(f"/playlists/{missing_playlist_id}")
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Playlist not found"}


def test_playlist_create_and_patch_invalid_payload_return_422(client: TestClient) -> None:
    create_with_missing_name_response = client.post(
        "/playlists/",
        json={},
    )
    assert create_with_missing_name_response.status_code == 422

    create_with_extra_field_response = client.post(
        "/playlists/",
        json={
            "name": "Unexpected Field Playlist",
            "unexpected_field": True,
        },
    )
    assert create_with_extra_field_response.status_code == 422

    valid_playlist_response = client.post("/playlists/", json={"name": "Patch Validation"})
    assert valid_playlist_response.status_code == 201
    playlist_id = valid_playlist_response.json()["id"]

    patch_with_empty_name_response = client.patch(
        f"/playlists/{playlist_id}",
        json={"name": ""},
    )
    assert patch_with_empty_name_response.status_code == 422

    patch_with_invalid_song_ids_response = client.patch(
        f"/playlists/{playlist_id}",
        json={"song_ids": [0]},
    )
    assert patch_with_invalid_song_ids_response.status_code == 422


def test_playlist_rejects_nonexistent_song_ids_on_create_and_patch(client: TestClient) -> None:
    create_with_missing_song_response = client.post(
        "/playlists/",
        json={
            "name": "Invalid Song Link",
            "song_ids": [99999],
        },
    )
    assert create_with_missing_song_response.status_code == 404
    assert create_with_missing_song_response.json() == {"detail": "Songs not found: [99999]"}

    valid_playlist_response = client.post("/playlists/", json={"name": "Patch Missing Song"})
    assert valid_playlist_response.status_code == 201
    playlist_id = valid_playlist_response.json()["id"]

    patch_with_missing_song_response = client.patch(
        f"/playlists/{playlist_id}",
        json={"song_ids": [99999]},
    )
    assert patch_with_missing_song_response.status_code == 404
    assert patch_with_missing_song_response.json() == {"detail": "Songs not found: [99999]"}
