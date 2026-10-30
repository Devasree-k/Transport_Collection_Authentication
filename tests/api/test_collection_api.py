import pytest

@pytest.mark.asyncio
async def test_list_collections_requires_authentication(client):
    response = await client.get("/api/collections/")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_collection_requires_authentication(client):
    response = await client.get("/api/collections/1")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_collection_requires_authentication(client):
    response = await client.post("/api/collections/", json={})
    assert response.status_code == 401
