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
def dummy_upsert_profile_data():
    user: UserUpsert = UserUpsertDataFactory.create()
    yield user.model_dump()


class TestUserAPI:
    def test_retrieve_profile(self, authenticated_client):
        client, authed_user = authenticated_client

        url = client.app.url_path_for("retrieve_profile")
        response = client.get(url)

        assert response.status_code == 200
        assert response.json()["id"] == authed_user.id
        assert response.json()["username"] == authed_user.username
        assert response.json()["email"] == authed_user.email

    def test_update_user(self, authenticated_client, dummy_upsert_profile_data):
        client, authed_user = authenticated_client

        url = client.app.url_path_for("update_profile")
        response = client.put(url, json=dummy_upsert_profile_data)

        assert response.status_code == 200
        updated_profile = response.json()

        assert updated_profile["username"] == dummy_upsert_profile_data["username"]
        assert updated_profile["email"] == dummy_upsert_profile_data["email"]
        assert updated_profile["name"] == dummy_upsert_profile_data["name"]
        assert updated_profile["surname"] == dummy_upsert_profile_data["surname"]

    def test_partial_update_user(self, authenticated_client):
        client, authed_user = authenticated_client

        url = client.app.url_path_for("partial_update_profile")
        response = client.patch(url, json={"name": "TestName"})

        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "TestName"

    def test_delete_user(self, authenticated_client):
        client, authed_user = authenticated_client

        delete_url = client.app.url_path_for("delete_profile")
        retrieve_url = client.app.url_path_for("retrieve_profile")

        response = client.delete(delete_url)
        assert response.status_code == 200

        response = client.get(retrieve_url)
        assert response.status_code == 404


class TestUserAPIEdgeCases:
    def test_retrieve_profile_unauthenticated(self, client):
        url = client.app.url_path_for("retrieve_profile")
        response = client.get(url)
        assert response.status_code == 401

    def test_update_user(self, client, dummy_upsert_profile_data):
        url = client.app.url_path_for("update_profile")
        response = client.put(url, json=dummy_upsert_profile_data)
        assert response.status_code == 401

    def test_partial_update_user(self, client):
        url = client.app.url_path_for("partial_update_profile")
        response = client.patch(url, json={"name": "TestName"})
        assert response.status_code == 401

    def test_delete_user(self, client):
        delete_url = client.app.url_path_for("delete_profile")
        response = client.delete(delete_url)
        assert response.status_code == 401


class TestRegistration:
    def test_create_user(self, client, dummy_upsert_profile_data):
        url = client.app.url_path_for("register")
        response = client.post(url, json=dummy_upsert_profile_data)

        assert response.status_code == 201
        created_user = response.json()
        assert created_user["username"] == dummy_upsert_profile_data["username"]
        assert created_user["email"] == dummy_upsert_profile_data["email"]

    def test_create_user_with_invalid_data(self, client, dummy_upsert_profile_data):
        url = client.app.url_path_for("register")

        invalid_data = dummy_upsert_profile_data
        del invalid_data["username"]

        response = client.post(url, json=invalid_data)

        assert response.status_code == 422
