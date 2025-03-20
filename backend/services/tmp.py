scrapped_data = {
    "book": {
        "publisher": "Scholastic",
        "synopsis": "Harry Potter has never been the star of a Quidditch team, scoring points while riding a broom far above the ground. He knows no spells, has never helped to hatch a dragon, and has never worn a cloak of invisibility.<br/><br/>All he knows is a miserable life with the Dursleys, his horrible aunt and uncle, and their abominable son, Dudley - a great big swollen spoiled bully. Harry's room is a tiny closet at the foot of the stairs, and he hasn't had a birthday party in eleven years.<br/><br/>But all that is about to change when a mysterious letter arrives by owl messenger: a letter with an invitation to an incredible place that Harry - and anyone who reads about him - will find unforgettable.",
        "language": "en",
        "image": "https://images.isbndb.com/covers/19044733482664.jpg",
        "title_long": "Harry Potter and the Sorcerer's Stone",
        "edition": "1",
        "dimensions": "Height: 7.75 Inches, Length: 5.25 Inches, Weight: 0.5 Pounds, Width: 0.75 Inches",
        "dimensions_structured": {
            "length": {
                "unit": "inches",
                "value": 5.25
            },
            "width": {
                "unit": "inches",
                "value": 0.7
            },
            "weight": {
                "unit": "pounds",
                "value": 0.5
            },
            "height": {
                "unit": "inches",
                "value": 7.5
            }
        },
        "pages": 309,
        "date_published": "1998-09",
        "subjects": [
            "Children's Books",
            "Growing Up & Facts of Life",
            "Family Life",
            "Friendship, Social Skills & School Life",
            "Humor",
            "Science Fiction & Fantasy",
            "Fantasy & Magic",
            "Teen & Young Adult",
            "Literature & Fiction",
            "Humorous",
            "Social & Family Issues",
            "Fantasy",
            "Self Service",
            "Custom Stores"
        ],
        "authors": [
            "J.K. Rowling"
        ],
        "title": "Harry Potter and the Sorcerer's Stone",
        "isbn13": "9781338878929",
        "msrp": "0.00",
        "binding": "Paperback",
        "isbn": "1338878921",
        "isbn10": "1338878921"
    }
}

from schemas.author_schema import AuthorCreate
from schemas.book_schema import BookAutomaticCreationByIsbn


# Author
author_data: str = scrapped_data["book"]["authors"][0]
author_name = author_data.split()[0][:author_data.find('.') + 1] if '.' in author_data else \
author_data.split()[0]
author_surname = author_data.split()[1] if len(author_data.split()) > 1 else ""
author_schema = AuthorCreate(name=author_name, surname=author_surname)

# Book details
title: str = scrapped_data["book"]["title"]
description: str = scrapped_data["book"]["synopsis"]

book_schema = BookAutomaticCreationByIsbn()
