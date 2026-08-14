import uuid

from httpx import AsyncClient


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_create_and_get_project(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/projects", json={"title": "Test project", "description": "for testing"}
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Test project"
    assert created["status"] == "todo"

    get_response = await client.get(f"/api/v1/projects/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


async def test_list_projects(client: AsyncClient) -> None:
    await client.post("/api/v1/projects", json={"title": "Project A"})
    await client.post("/api/v1/projects", json={"title": "Project B"})

    response = await client.get("/api/v1/projects")
    assert response.status_code == 200
    titles = {p["title"] for p in response.json()}
    assert titles == {"Project A", "Project B"}


async def test_patch_project_partial_update(client: AsyncClient) -> None:
    create_response = await client.post("/api/v1/projects", json={"title": "Original"})
    project_id = create_response.json()["id"]

    patch_response = await client.patch(
        f"/api/v1/projects/{project_id}", json={"status": "in_progress"}
    )
    assert patch_response.status_code == 200
    body = patch_response.json()
    assert body["status"] == "in_progress"
    assert body["title"] == "Original"  # untouched field stays as-is


async def test_delete_project(client: AsyncClient) -> None:
    create_response = await client.post("/api/v1/projects", json={"title": "To delete"})
    project_id = create_response.json()["id"]

    delete_response = await client.delete(f"/api/v1/projects/{project_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/projects/{project_id}")
    assert get_response.status_code == 404


async def test_get_nonexistent_project(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/projects/{uuid.uuid4()}")
    assert response.status_code == 404
