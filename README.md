# Book Review Platform

## Description
A platform where users can write and read book reviews, rate books, and get personalized recommendations based on their reading history.

## Tech Stack
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- **Authentication**: [JWT](https://jwt.io/)
- **Testing**: [pytest](https://pytest.org/)
- **CI Workflows**: GitHub Actions for running tests and checking code style

## Key Features
- **User Authentication**: Secure authentication with JWT tokens.
- **Profile Management**:
  - Retrieve information about the user's profile.
  - Update profile.
  - Patch profile.
  - Delete profile.

## How to use
### Docker
- docker-compose up --build

### Manually
- Start fastapi server: <br>
  ```python -m uvicorn main:app --port 8000 --reload```
- Database:
  - Migrations:
    - Generate migrations <br>
      ```python -m alembic revision --autogenerate -m "Your message here"```
    - Apply migrations <br>
      ```python -m alembic upgrade head```
    - Rollback migration \
      - `python -m alembic downgrade <revision_id>`
      - `python -m alembic downgrade -1`
  - psql:
    - Connect to db: <br>
      ```psql -h <hostname> -p <port> -d <database_name> -U <username>```
    - List all databases: \
      `\l`
    - List tables: \
      `\dt`
    - Print table structure: \
      `\d <table_name>`
- Run tests: <br>
  ```python -m pytest"```
- Run linter: <br>
  ```python -m flake8"```
