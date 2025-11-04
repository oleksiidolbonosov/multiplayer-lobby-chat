import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_list_room():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        resp = await ac.post('/lobby/create', json={'name':'demo','max_players':4})
        assert resp.status_code == 200
        room = resp.json()
        assert 'id' in room and room['name'] == 'demo'
        resp2 = await ac.get('/lobby/list')
        assert resp2.status_code == 200
        rooms = resp2.json()
        assert any(r['name']=='demo' for r in rooms)
