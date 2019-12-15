import datetime
import unittest
from random import randint

from app.main import db
from app.main.models.book import Writer, Book, Rating
from app.main.models.user import User
from app.tests.base import BaseTestCase


class TestWriterModel(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        self.writer = Writer(
            first_name='Test',
            last_name='Test'
        )
        self.writer_books = [Book(name=f'Book{i}', authors=[self.writer]) for i in range(10)]
        db.session.add(self.user)
        db.session.add(self.writer)
        db.session.add_all(self.writer_books)
        db.session.commit()
        self.ratings = [Rating(user_id=self.user.id, book_id=book.id, value=randint(1, 5)) for book in self.writer_books]
        db.session.add_all(self.ratings)
        db.session.commit()

    def test_full_name(self):
        self.assertEqual(self.writer.full_name, 'Test Test')

    def test_top_books(self):
        top_books = self.writer.top_books
        self.assertEqual(len(top_books), 5)
        for ind in range(len(top_books) - 1):
            self.assertTrue(top_books[ind].rating >= top_books[ind + 1].rating)


if __name__ == '__main__':
    unittest.main()
