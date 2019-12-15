import datetime
import unittest
from random import randint

from app.main import db
from app.main.models.book import Writer, Book, Rating
from app.main.models.user import User
from app.tests.base import BaseTestCase


class TestBookModel(BaseTestCase):

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

    def test_ratings_value(self):
        avg = sum(rating.value for rating in self.ratings) / self.ratings_len
        self.assertEqual(self.book.rating, avg)


if __name__ == '__main__':
    unittest.main()
