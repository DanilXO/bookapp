import datetime
import unittest
from random import randint

from app.main import db
from app.main.models.book import Book, Rating
from app.main.models.user import User
from app.main.services.book_service import get_book, delete_book, update_book, add_book_rating, save_new_book
from app.tests.base import BaseTestCase


class TestBookService(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(self.user)
        self.book = Book(
            name='Test'
        )
        db.session.add(self.user)
        db.session.add(self.book)
        db.session.commit()
        self.ratings_len = 5
        self.ratings = [Rating(user_id=self.user.id, book_id=self.book.id, value=randint(1, 5))
                        for _ in range(self.ratings_len)]
        db.session.add_all(self.ratings)
        db.session.commit()

    def test_get_book(self):
        book_from_db = get_book(self.book.id)
        self.assertEqual(self.book, book_from_db)

    def test_delete_book(self):
        book_for_delete = Book(
            name='TestForDelete'
        )
        db.session.add(book_for_delete)
        db.session.commit()
        deleted_book_id = book_for_delete.id
        success_response_object = {
            'status': 'success',
            'message': 'Book successfully deleted.',
        }
        fail_response_object = {
            'status': 'fail',
            'message': 'Book does not exists.',
        }
        response_object, code = delete_book(deleted_book_id)
        self.assertEqual(response_object, success_response_object)
        self.assertEqual(code, 204)
        response_object, code = delete_book(9999)
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 404)

    def test_update_book(self):
        new_name = 'New Name'
        new_authors = [{'first_name':'Jack', 'last_name': 'Palanik'}]
        success_response_object = {
            'status': 'success',
            'message': 'Book successfully updated.',
        }
        fail_response_object = {
            'status': 'fail',
            'message': 'Book does not exists.',
        }
        response_object, code = update_book(self.book.id, {'name': new_name, 'authors': new_authors})
        self.assertEqual(response_object, success_response_object)
        self.assertEqual(code, 204)
        self.assertEqual(self.book.name, new_name)
        prev_name = self.book.name
        response_object, code = update_book(999, {'name': new_name, 'authors': new_authors})
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 404)
        self.assertEqual(self.book.name, prev_name)

    def test_add_book_rating(self):
        book_with_empty_rating = Book(
            name='book_with_empty_rating'
        )
        db.session.add(book_with_empty_rating)
        db.session.commit()
        rating_value = 4
        success_response_object = {
            'status': 'success',
            'message': 'New rating for book successfully added.',
        }
        fail_response_object = {
            'status': 'fail',
            'message': 'Book or user does not exists.',
        }
        response_object, code = add_book_rating(self.user.id, book_with_empty_rating.id, {'value': rating_value})
        self.assertEqual(response_object, success_response_object)
        self.assertEqual(code, 201)
        self.assertEqual(book_with_empty_rating.rating, rating_value)
        response_object, code = add_book_rating(self.user.id, 999, {'value': rating_value})
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 404)
        response_object, code = add_book_rating(999, book_with_empty_rating.id, {'value': rating_value})
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 404)
        with self.assertRaises(AssertionError):
            add_book_rating(999, book_with_empty_rating.id, {'value': 999})

    def test_save_new_book(self):
        new_book_data = {
            'name': 'New book'
        }
        success_response_object = {
            'status': 'success',
            'message': 'Book successfully created.',
        }
        fail_response_object = {
            'status': 'fail',
            'message': 'Book already exists. Please try other name.',
        }
        response_object, code = save_new_book(new_book_data)
        self.assertEqual(response_object, success_response_object)
        self.assertEqual(code, 201)
        response_object, code = save_new_book({'name': self.book.name})
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 409)


if __name__ == '__main__':
    unittest.main()
