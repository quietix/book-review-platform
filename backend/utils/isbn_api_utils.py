import requests

from config import config, logger
from excepitons.isbn_api_exceptions import IsbnAPIException

from schemas.author_schema import AuthorCreate
from schemas.book_schema import BookAutomaticCreationByIsbn


async def get_data_by_isbn(isbn: str) -> dict:
    try:
        headers = {'Authorization': config.ISBNDB_API_KEY}
        response = requests.get(f"{config.ISBNDB_API_URL}/{isbn}", headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        exc = IsbnAPIException(status_code=504,
                               detail="Request to the external ISBN API timed out.")
        logger.error(exc.detail)
        raise exc

    except requests.exceptions.ConnectionError:
        exc = IsbnAPIException(status_code=502,
                               detail="Could not connect to the external ISBN API.")
        logger.error(exc.detail)
        raise exc

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            exc = IsbnAPIException(status_code=404,
                                   detail="Book not found for the given ISBN.")
            logger.error(exc.detail)
            raise exc

        elif e.response.status_code == 401:
            exc = IsbnAPIException(status_code=401,
                                   detail="Unauthorized access to the ISBN API.")
            logger.error(exc.detail)
            raise exc

        elif e.response.status_code == 503:
            exc = IsbnAPIException(status_code=503,
                                   detail="The external ISBN API is currently unavailable.")
            logger.error(exc.detail)
            raise exc

        else:
            exc = IsbnAPIException()
            logger.error(exc.detail)
            raise exc

    except Exception as e:
        exc = IsbnAPIException()
        logger.error(f"{exc.detail}. Details: {e}")
        raise exc


async def scrap_author_data(scrapped_data: dict) -> AuthorCreate:
    try:
        author_data: str = scrapped_data["book"]["authors"][0]
        author_name = author_data.split()[0][:author_data.find('.') + 1] if '.' in author_data \
            else author_data.split()[0]
        author_surname = author_data.split()[-1] if len(author_data.split()) > 1 else ""
        logger.debug(f"author_data = {author_data}")
        logger.debug(f"author_name = {author_name}")
        logger.debug(f"author_surname = {author_surname}")
        author_schema = AuthorCreate(name=author_name, surname=author_surname)
        return author_schema

    except Exception as e:
        exc = IsbnAPIException()
        logger.error(f"{exc.detail}. Details: {e}")
        raise exc


async def scrap_book_data(scrapped_data: dict) -> BookAutomaticCreationByIsbn:
    try:
        title: str = scrapped_data["book"]["title"]
        description: str = scrapped_data["book"]["synopsis"]

        book_schema = BookAutomaticCreationByIsbn(title=title, description=description)
        return book_schema

    except Exception as e:
        exc = IsbnAPIException()
        logger.error(f"{exc.detail}. Details: {e}")
        raise exc
