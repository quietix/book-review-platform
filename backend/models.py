from datetime import datetime

from sqlalchemy import (
    String,
    LargeBinary,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    surname: Mapped[str] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary)
    is_admin: Mapped[bool] = mapped_column(default=False)

    published_authors = relationship("Author", back_populates="publisher")
    published_books = relationship("Book", back_populates="publisher")
    published_reviews = relationship("Review", back_populates="publisher")
    ratings = relationship("Rating", back_populates="user")
    reading_items = relationship("ReadingItem", back_populates="user")


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    publisher_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    publisher = relationship("User", back_populates="published_authors")

    name: Mapped[str] = mapped_column(String(255))
    surname: Mapped[str] = mapped_column((String(255)))
    published_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    books = relationship("Book", back_populates="author", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint("name", "surname", name="uq_author_name_surname"),
    )


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    genre: Mapped[str] = mapped_column(String(255))

    books = relationship("Book", back_populates="genre")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id", ondelete="CASCADE"))
    author = relationship("Author", back_populates="books")

    publisher_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    publisher = relationship("User", back_populates="published_books")

    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"), nullable=True)
    genre = relationship("Genre", back_populates="books")

    isbn: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    published_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    reviews = relationship("Review", back_populates="book")
    ratings = relationship("Rating", back_populates="book")
    reading_items = relationship("ReadingItem", back_populates="book")


class Rating(Base):
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book = relationship("Book", back_populates="ratings")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="ratings")

    rating: Mapped[int] = mapped_column(
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_rating")
    )

    reviews = relationship("Review", back_populates="rating")


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    publisher_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    publisher = relationship("User", back_populates="published_reviews")

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book = relationship("Book", back_populates="reviews")

    rating_id: Mapped[int] = mapped_column(ForeignKey("rating.id"), nullable=True)
    rating = relationship("Rating", back_populates="reviews")

    title: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(nullable=True)

    published_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(255))

    reading_items = relationship("ReadingItem", back_populates="status")


class ReadingItem(Base):
    __tablename__ = "reading_list"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="reading_items")

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book = relationship("Book", back_populates="reading_items")

    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    status = relationship("Status", back_populates="reading_items")
