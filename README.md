# Book Review Platform

## Description
This is the backend part of a platform where users can write and read book reviews, rate books, and get personalized recommendations based on their reading history.

## Table of contents
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [How to use](#installation-and-launch)
- [May be useful](#may-be-useful)

## Tech Stack
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- **Authentication**: [JWT](https://en.wikipedia.org/wiki/JSON_Web_Token)
- **Testing**: [Pytest](https://pytest.org/)
- **Launch**: [Docker](https://www.docker.com/)
- **GitHub Actions**: [GitHub Actions](https://docs.github.com/en/actions)

## Key Features
- **User Authentication**: \
  JWT bearer tokens
- **Profile Management**:
  - CRUD operations for user's profile
  - User can interact only with their own profile

- **Authors Management**:
  - CRUD operations for Book's Authors
  - User is recorded as the publisher of the Author
  - Only the Author's publisher can modify the Author

- **Genres Management**:
  - CRUD operations for Genres
  - Genres creation/modification is available only to the admin user

- **Books Management**:
  - Basic CRUD operations for Books with additional options:
    - Create Book manually: \
      User is recorded as the publisher of the Book
    - Create Book by its isbn: \
      Nobody is recorded as the publisher of the Book. The book cannot be changed. \
      Information about the Book and its Author is fetched from [isbndb](https://isbndb.com/apidocs/v2)
  - Only the Book's publisher can modify the Book

- **Rating Management**:
  - CRUD operations for Rating
  - User is recorded as the publisher of the Rating
  - User can rate the same book only once
  - Only the Rating's owner can modify the Rating

- **Review Management**:
  - CRUD operations for Review
  - User is recorded as the publisher of the Review
  - User can create Review for the same book only once
  - Only the Review's owner can modify the Review
  - Review's Rating can be created in 2 ways:
    - Separately, then the Rating's id must be referenced inside the Review
    - During Review creation, then a new Rating record is created and automatically referenced

- **Status Management**:
  - CRUD operations for Status
  - Statuses creation/modification is available only to the admin user
  - Needed for ReadingItem entity
  - Status examples for better understanding: `Want to read`, `Finished`

- **Reading Item Management**:
  - CRUD operations for ReadingItem
  - User is recorded as the owner of the ReadingItem
  - User can create only one ReadingItem for the same book  
  - Only the ReadingItem's owner can modify the ReadingItem
  - Maps Statuses, Users and Books
  - Is used for recommendations feature 

- **Recommendations based on reading history**: \
  If user has Finished books, they can receive recommendations based on the 
  author of the most recent book they've read. Recommended books are sorted by
  their average rating.

## Installation and Launch
1. Clone the repository
2. Set up Environment Variables:
    - Create a .env file in the root directory
    - Populate the .env file with the environment variables
3. Build and run using Docker Compose:
    - Ensure you have [Docker](https://www.docker.com/get-started/) installed and launched
    - From the root directory of the project, run:
      ```
      docker-compose up --build -d
      ```

## May be useful
- Follow Docker Compose logs: \
  `docker-compose logs -f`
- Start fastapi server: \
  `python -m uvicorn main:app --port 8000 --reload`
- Database:
  - Migrations:
    - Generate migrations \
      `python -m alembic revision --autogenerate -m "Your message here"`
    - Apply migrations \
      `python -m alembic upgrade head`
    - Rollback migration
      - `python -m alembic downgrade <revision_id>`
      - `python -m alembic downgrade -1`
  - psql:
    - Connect to db: \
      `psql -h <hostname> -p <port> -d <database_name> -U <username>`
    - List all databases: \
      `\l`
    - List tables: \
      `\dt`
    - Print table structure: \
      `\d <table_name>`
- Run tests: \
  `python -m pytest`
- Run linter: \
  `python -m flake8`
