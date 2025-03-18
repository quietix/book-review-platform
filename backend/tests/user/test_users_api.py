import pytest

from tests.factories import UserFactory, UserUpsertDataFactory
from schemas import UserUpsert


@pytest.fixture
def dummy_users():
    yield UserFactory.create_batch(5)


@pytest.fixture
def dummy_user():
    yield UserFactory.create()


@pytest.fixture
def dummy_upsert_user_data():
    user: UserUpsert = UserUpsertDataFactory.create()
    yield user.model_dump()


class TestUserAPI:
    def test_list_user(self, client, dummy_users):
        url = client.app.url_path_for("list_users")
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.json()) == len(dummy_users)

    def test_create_user(self, client, dummy_upsert_user_data):
        url = client.app.url_path_for("create_user")
        response = client.post(url, json=dummy_upsert_user_data)

        assert response.status_code == 201
        created_user = response.json()
        assert created_user["username"] == dummy_upsert_user_data["username"]
        assert created_user["email"] == dummy_upsert_user_data["email"]

    def test_update_user(self, client, dummy_user, dummy_upsert_user_data):
        url = client.app.url_path_for("update_user", user_id=dummy_user.id)
        response = client.put(url, json=dummy_upsert_user_data)

        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["username"] == dummy_upsert_user_data["username"]
        assert updated_user["email"] == dummy_upsert_user_data["email"]
        assert updated_user["name"] == dummy_upsert_user_data["name"]
        assert updated_user["surname"] == dummy_upsert_user_data["surname"]

    def test_partial_update_user(self, client, dummy_user):
        url = client.app.url_path_for("partial_update_user", user_id=dummy_user.id)
        response = client.patch(url, json={"name": "TestName"})

        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "TestName"

    def test_delete_user(self, client, dummy_user):
        delete_url = client.app.url_path_for("delete_user", user_id=dummy_user.id)
        retrieve_url = client.app.url_path_for("retrieve_user", user_id=dummy_user.id)

        response = client.delete(delete_url)

        assert response.status_code == 200

        response = client.get(retrieve_url)
        assert response.status_code == 404


class TestUserAPIEdgeCases:
    def test_create_user_with_invalid_data(self, client, dummy_upsert_user_data):
        url = client.app.url_path_for("create_user")

        invalid_data = dummy_upsert_user_data
        del invalid_data["username"]

        response = client.post(url, json=invalid_data)

        assert response.status_code == 422

    def test_update_non_existent_user(self, client, dummy_upsert_user_data):
        non_existent_user_id = 99999

        url = client.app.url_path_for("update_user", user_id=non_existent_user_id)
        response = client.put(url, json=dummy_upsert_user_data)

        assert response.status_code == 404

    def test_partial_update_non_existent_user(self, client, dummy_upsert_user_data):
        non_existent_user_id = 99999

        url = client.app.url_path_for("partial_update_user", user_id=non_existent_user_id)
        response = client.patch(url, json=dummy_upsert_user_data)

        assert response.status_code == 404

    def test_delete_non_existent_user(self, client):
        non_existent_user_id = 99999
        url = client.app.url_path_for("delete_user", user_id=non_existent_user_id)
        response = client.delete(url)

        assert response.status_code == 404
