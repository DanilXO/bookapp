from app.main import db
from app.main.models.book import Book, Rating, Writer
from app.main.models.user import User
from app.main.services.pagination_helper import get_paginated_list
from app.main.services.user_service import save_changes
from app.main.utils.tools import get_or_create


def get_books_by_page(api, marshal_object, page_num, base_url):
    return get_paginated_list(api, marshal_object, Book, page_num, base_url)


def get_book(book_id):
    return Book.query.filter_by(id=book_id).first()


def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Book successfully deleted.',
        }
        return response_object, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'Book does not exists.',
        }
        return response_object, 404


def update_book(book_id, data):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        if data:
            authors_data = data.get('authors')
            if authors_data:
                authors = []
                for author_data in authors_data:
                    author = get_or_create(db, Writer, first_name=author_data.get('first_name'),
                                           last_name=author_data.get('last_name'))
                    authors.append(author)
                book.authors = authors
            new_name = data.get('name')
            if new_name:
                book.name = new_name
            save_changes(book)
        response_object = {
            'status': 'success',
            'message': 'Book successfully updated.',
        }
        return response_object, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'Book does not exists.',
        }
        return response_object, 404


def add_book_rating(user_id, book_id, data):
    rating_exists = Rating.query.filter_by(user_id=user_id, book_id=book_id).first()
    value = data['value']
    book = Book.query.filter_by(id=book_id).first()
    user = User.query.filter_by(id=user_id).first()
    if not book or not user:
        response_object = {
            'status': 'fail',
            'message': 'Book or user does not exists.',
        }
        return response_object, 404
    else:
        if not rating_exists:
            new_rating = Rating(
                user_id=user.id,
                book_id=book.id,
                value=value
            )
            save_changes(new_rating)
        else:
            rating_exists.value = value
            save_changes(rating_exists)
        response_object = {
            'status': 'success',
            'message': 'New rating for book successfully added.',
        }
        return response_object, 201


def save_new_book(data):
    book_exists = Book.query.filter_by(name=data['name']).first()
    if not book_exists:
        authors_data = data['authors']
        authors = []
        for author_data in authors_data:
            author = get_or_create(db, Writer, first_name=author_data.get('first_name'),
                                   last_name=author_data.get('last_name'))
            authors.append(author)
        new_book = Book(
            name=data['name'],
            authors=authors
        )
        save_changes(new_book)
        response_object = {
            'status': 'success',
            'message': 'Book successfully created.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Book already exists. Please try other name.',
        }
        return response_object, 409
