from fastapi.testclient import TestClient


def create_song(
    client: TestClient,
    **overrides: object,
) -> dict:
    payload = {
        "title": "Numb",
        "artist": "Linkin Park",
        "album": "Meteora",
        "genre": "Rock",
        "duration_seconds": 185,
        "release_year": 2003,
    }
    payload.update(overrides)

    response = client.post("/songs/", json=payload)
    assert response.status_code == 201
    return response.json()


def test_song_create_and_list_contract(client: TestClient) -> None:
    created_song = create_song(client)
    song_id = created_song["id"]

    assert created_song["title"] == "Numb"
    assert created_song["artist"] == "Linkin Park"
    assert created_song["genre"] == "Rock"
    assert created_song["duration_seconds"] == 185

    list_response = client.get("/songs/")
    assert list_response.status_code == 200
    listed_songs = list_response.json()
    assert any(song["id"] == song_id for song in listed_songs)


def test_song_get_by_id_returns_created_song(client: TestClient) -> None:
    created_song = create_song(client)
    song_id = created_song["id"]

    read_response = client.get(f"/songs/{song_id}")
    assert read_response.status_code == 200

    read_song = read_response.json()
    assert read_song["id"] == song_id
    assert read_song["title"] == "Numb"
    assert read_song["genre"] == "Rock"


def test_song_patch_updates_only_expected_fields(client: TestClient) -> None:
    created_song = create_song(client)
    song_id = created_song["id"]

    update_response = client.patch(f"/songs/{song_id}", json={"genre": "Alternative Rock"})
    assert update_response.status_code == 200

    updated_song = update_response.json()
    assert updated_song["genre"] == "Alternative Rock"
    assert updated_song["title"] == "Numb"
    assert updated_song["duration_seconds"] == 185


def test_song_delete_removes_song(client: TestClient) -> None:
    created_song = create_song(client)
    song_id = created_song["id"]

    delete_response = client.delete(f"/songs/{song_id}")
    assert delete_response.status_code == 204

    read_deleted_response = client.get(f"/songs/{song_id}")
    assert read_deleted_response.status_code == 404
    assert read_deleted_response.json() == {"detail": "Song not found"}


def test_song_missing_id_returns_404_for_get_patch_and_delete(client: TestClient) -> None:
    missing_song_id = 99999

    get_response = client.get(f"/songs/{missing_song_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Song not found"}

    patch_response = client.patch(f"/songs/{missing_song_id}", json={"genre": "Any Genre"})
    assert patch_response.status_code == 404
    assert patch_response.json() == {"detail": "Song not found"}

    delete_response = client.delete(f"/songs/{missing_song_id}")
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Song not found"}


def test_create_song_with_invalid_payload_returns_422(client: TestClient) -> None:
    missing_required_field_response = client.post(
        "/songs/",
        json={
            "title": "Missing Artist",
        },
    )
    assert missing_required_field_response.status_code == 422

    invalid_duration_response = client.post(
        "/songs/",
        json={
            "title": "Invalid Duration",
            "artist": "Unknown",
            "duration_seconds": 0,
        },
    )
    assert invalid_duration_response.status_code == 422

    invalid_field_type_response = client.post(
        "/songs/",
        json={
            "title": {"unexpected": "object"},
            "artist": "Unknown",
            "duration_seconds": 180,
        },
    )
    assert invalid_field_type_response.status_code == 422
