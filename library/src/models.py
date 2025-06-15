class Author:
    def __init__(self, id, first_name, last_name, birth_year, nationality):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.nationality = nationality

class Book:
    def __init__(self, id, title, author_id, publication_year, genre, pages, description):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.publication_year = publication_year
        self.genre = genre
        self.pages = pages
        self.description = description