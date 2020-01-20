from sqlalchemy import func, desc
from sqlalchemy.ext.hybrid import hybrid_property

from .. import db


class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    value = db.Column(db.Integer)

    @db.validates('value')
    def validate_value(self, key, value):
        assert 1 <= value <= 5
        return value

    def __repr__(self):
        return '<User[{}] set Book[{}] {} stars>'.format(self.user_id, self.book_id, self.value)


association_w_b = db.Table('association_w_b',
                           db.Column('writer_id', db.Integer, db.ForeignKey('writer.id'), primary_key=True),
                           db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
                           )


class Writer(db.Model):
    __tablename__ = 'writer'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def top_books(self):
        return Book.query.filter(Book.authors.any(id=self.id)).order_by(
            desc(Book.rating_sum / Book.rating_count)).limit(5).all()

    def __repr__(self):
        return '<Writer {}>'.format(self.full_name)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    authors = db.relationship('Writer', secondary=association_w_b, lazy='subquery',
                              backref=db.backref('books', lazy=True))
    _ratings = db.relationship('Rating', backref='book', lazy='dynamic')
    rating_sum = db.Column(db.Integer)
    rating_count = db.Column(db.Integer)

    @property
    def rating(self):
        return self.rating_sum / self.rating_count if self.rating_count is not None and self.rating_count > 0 else 1

    def add_rating_count(self):
        if self.rating_count:
            self.rating_count += 1
        else:
            self.rating_count = 1

    def add_rating_sum(self, value):
        if self.rating_sum:
            self.rating_sum += value
        else:
            self.rating_sum = value

    def sub_rating_sum(self, value):
        if self.rating_sum:
            self.rating_sum -= value

    # Первая идея, не самая удачная, так как с увеличением рейтинга будет увеличиваться время просчета и
    # выполнения запроса. Решил отказаться в пользу сохранения количества и суммы рейтинга.
    # @hybrid_property
    # def rating(self):
    #     average = db.session.query(func.avg(Rating.value)\
    # .label('average')).filter(Rating.book_id == self.id).first()[0]
    #     return average if average else 1
    #
    # @rating.expression
    # def rating(cls):
    #     return db.session.query(func.avg(Rating.value).label('average')).filter(Rating.book_id == cls.id)

    def __repr__(self):
        return '<Book {}>'.format(self.name)
