from app import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    rating = db.relationship('Rating', backref='user', lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Rating(db.Model):
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


association_w_b = db.Table('tags',
                           db.Column('writer_id', db.Integer, db.ForeignKey('writer.id'), primary_key=True),
                           db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
                           )


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)

    @property
    def full_name(self):
        return f"{self.first_name}{self.last_name}"

    def __repr__(self):
        return '<Writer {}>'.format(self.full_name)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    author = db.relationship('Writer', secondary=association_w_b, lazy='subquery',
                             backref=db.backref('books', lazy=True))
    rating = db.relationship('Rating', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Book {}>'.format(self.username)
