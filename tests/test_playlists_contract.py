from fastapi.testclient import TestClient


def create_playlist(
    client: TestClient,
    **overrides: object,
) -> dict:
    payload = playlist_expectations()
    payload.pop("songs")
    payload.update(overrides)

    response = client.post("/playlists/", json=payload)
    assert response.status_code == 201
    return response.json()


def playlist_expectations(**overrides: object) -> dict[str, object]:
    expected_payload = {
        "name": "Daily Mix",
        "description": "Work playlist",
        "is_public": True,
        "songs": [],
    }
    expected_payload.update(overrides)
    return expected_payload


def assert_playlist_payload(
    playlist: dict,
    expected: dict[str, object],
) -> None:
    actual_payload = {field_name: playlist[field_name] for field_name in expected}
    assert actual_payload == expected


def assert_playlist_not_found(response) -> None:
    assert response.status_code == 404
    assert response.json() == {"detail": "Playlist not found"}


def test_playlist_create_returns_expected_payload(client: TestClient) -> None:
    created_playlist = create_playlist(client)

    assert_playlist_payload(created_playlist, playlist_expectations())


def test_playlist_list_includes_created_playlist(client: TestClient) -> None:
    created_playlist = create_playlist(client)

    list_response = client.get("/playlists/")
    assert list_response.status_code == 200

    listed_playlists = list_response.json()
    assert any(playlist["id"] == created_playlist["id"] for playlist in listed_playlists)


def test_playlist_get_by_id_returns_created_playlist(client: TestClient) -> None:
    created_playlist = create_playlist(client)

    read_response = client.get(f"/playlists/{created_playlist['id']}")
    assert read_response.status_code == 200

    read_playlist = read_response.json()
    assert read_playlist["id"] == created_playlist["id"]
    assert_playlist_payload(read_playlist, playlist_expectations())


def test_playlist_patch_updates_only_expected_fields(client: TestClient) -> None:
    created_playlist = create_playlist(client)

    patch_response = client.patch(
        f"/playlists/{created_playlist['id']}",
        json={
            "description": "Updated description",
            "is_public": False,
        },
    )
    assert patch_response.status_code == 200

    patched_playlist = patch_response.json()
    assert patched_playlist["id"] == created_playlist["id"]
    assert_playlist_payload(
        patched_playlist,
        playlist_expectations(
            description="Updated description",
            is_public=False,
        ),
    )


def test_playlist_delete_removes_playlist(client: TestClient) -> None:
    created_playlist = create_playlist(client)

    delete_response = client.delete(f"/playlists/{created_playlist['id']}")
    assert delete_response.status_code == 204

    read_deleted_response = client.get(f"/playlists/{created_playlist['id']}")
    assert_playlist_not_found(read_deleted_response)


def test_playlist_get_missing_id_returns_404(client: TestClient) -> None:
    response = client.get("/playlists/99999")

    assert_playlist_not_found(response)


def test_playlist_patch_missing_id_returns_404(client: TestClient) -> None:
    response = client.patch(
        "/playlists/99999",
        json={"description": "Any description"},
    )

    assert_playlist_not_found(response)


def test_playlist_delete_missing_id_returns_404(client: TestClient) -> None:
    response = client.delete("/playlists/99999")

    assert_playlist_not_found(response)


def test_playlist_create_missing_name_returns_422(client: TestClient) -> None:
    response = client.post("/playlists/", json={})

    assert response.status_code == 422


def test_playlist_create_extra_field_returns_422(client: TestClient) -> None:
    response = client.post(
        "/playlists/",
        json={
            "name": "Unexpected Field Playlist",
            "unexpected_field": True,
        },
    )

    assert response.status_code == 422


def test_playlist_patch_empty_name_returns_422(client: TestClient) -> None:
    created_playlist = create_playlist(client, name="Patch Validation")

    response = client.patch(
        f"/playlists/{created_playlist['id']}",
        json={"name": ""},
    )

    assert response.status_code == 422


def test_playlist_patch_invalid_song_ids_returns_422(client: TestClient) -> None:
    created_playlist = create_playlist(client, name="Patch Validation")

    response = client.patch(
        f"/playlists/{created_playlist['id']}",
        json={"song_ids": [0]},
    )

    assert response.status_code == 422


def test_playlist_create_nonexistent_song_ids_returns_404(client: TestClient) -> None:
    response = client.post(
        "/playlists/",
        json={
            "name": "Invalid Song Link",
            "song_ids": [99999],
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Songs not found: [99999]"}


def test_playlist_patch_nonexistent_song_ids_returns_404(client: TestClient) -> None:
    created_playlist = create_playlist(client, name="Patch Missing Song")

    response = client.patch(
        f"/playlists/{created_playlist['id']}",
        json={"song_ids": [99999]},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Songs not found: [99999]"}
