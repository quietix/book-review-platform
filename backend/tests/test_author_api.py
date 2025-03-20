import pytest

from tests.factories.author_factory import AuthorFactory, AuthorCreateDataFactory
from schemas.author_schema import AuthorCreate


@pytest.fixture
def dummy_authors():
    yield AuthorFactory.create_batch(5)


@pytest.fixture
def dummy_author():
    yield AuthorFactory.create()


@pytest.fixture
def dummy_upsert_author_data(dummy_author):
    author: AuthorCreate = AuthorCreateDataFactory.create()
    yield author.model_dump()


class TestAuthorAPI:
    def test_list_authors(self, client, dummy_authors):
        url = client.app.url_path_for("list_authors")
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.json()) == 5

    def test_create_user(self, authenticated_client, dummy_upsert_author_data):
        client, authed_user = authenticated_client

        url = client.app.url_path_for("create_author")
        response = client.post(url, json=dummy_upsert_author_data)

        assert response.status_code == 201
        created_author = response.json()
        assert created_author["publisher_id"] == authed_user.id
        assert created_author["name"] == dummy_upsert_author_data["name"]
        assert created_author["surname"] == dummy_upsert_author_data["surname"]

    def test_retrieve_author(self, authenticated_client, dummy_author):
        client, authed_user = authenticated_client

        url = client.app.url_path_for("retrieve_author", author_id=dummy_author.id)
        response = client.get(url)

        assert response.status_code == 200
        assert response.json()["id"] == dummy_author.id
        assert response.json()["name"] == dummy_author.name
        assert response.json()["surname"] == dummy_author.surname
        assert response.json()["publisher"]
        assert response.json()["published_at"]
        assert response.json()["updated_at"]

    def test_retrieve_author_unauthed(self, client, dummy_author):
        url = client.app.url_path_for("retrieve_author", author_id=dummy_author.id)
        response = client.get(url)
        assert response.status_code == 401

    def test_partial_update_author(self, authenticated_client):
        client, authed_user = authenticated_client
        dummy_author = AuthorFactory.create(publisher=authed_user)

        url = client.app.url_path_for("partial_update_author", author_id=dummy_author.id)
        response = client.patch(url, json={"name": "TestName"})

        assert response.status_code == 200
        assert response.json()["name"] == "TestName"

    def test_partial_update_author_unauthed(self, client, dummy_author):
        url = client.app.url_path_for("partial_update_author", author_id=dummy_author.id)
        response = client.patch(url, json={"name": "TestName"})
        assert response.status_code == 401

    def test_delete_author(self, authenticated_client):
        client, authed_user = authenticated_client
        dummy_author = AuthorFactory.create(publisher=authed_user)

        delete_url = client.app.url_path_for("delete_author", author_id=dummy_author.id)
        retrieve_url = client.app.url_path_for("retrieve_author", author_id=dummy_author.id)

        response = client.delete(delete_url)
        assert response.status_code == 200

        response = client.get(retrieve_url)
        assert response.status_code == 404

    def test_delete_author_unauthed(self, client, dummy_author):
        delete_url = client.app.url_path_for("delete_author", author_id=dummy_author.id)
        response = client.delete(delete_url)
        assert response.status_code == 401
