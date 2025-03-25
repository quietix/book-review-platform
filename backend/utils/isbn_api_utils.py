import httpx

from config import config, logger
from exceptions.isbn_api_exceptions import IsbnAPIException

from schemas.author_schema import AuthorCreate
from schemas.book_schema import BookAutomaticCreationByIsbn


async def get_data_by_isbn(isbn: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': config.ISBNDB_API_KEY}
            response = await client.get(f"{config.ISBNDB_API_URL}/{isbn}", headers=headers)
            response.raise_for_status()
            return response.json()

    except httpx.RequestError as e:
        logger.error(f"Error fetching data for ISBN {isbn}. Details: {e}")
        raise IsbnAPIException(detail=f"Error fetching data for ISBN {isbn}")

    except Exception as e:
        exc = IsbnAPIException()
        logger.error(f"Error fetching data for ISBN {isbn}. Details: {e}")
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
        book_data = scrapped_data["book"]
        if not book_data:
            exc = IsbnAPIException(detail="Failed to scrap book data.")
            logger.error(f"{exc.detail}")
            raise exc

        title: str = book_data.get("title")
        if not title:
            exc = IsbnAPIException(detail="Failed to scrap book title.")
            logger.error(f"{exc.detail}")
            raise exc

        description: str = book_data.get("synopsis")

        book_schema = BookAutomaticCreationByIsbn(title=title, description=description)

        return book_schema

    except Exception as e:
        exc = IsbnAPIException()
        logger.error(f"{exc.detail}. Details: {e}")
        raise exc
