from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class WriterIncludeDto:
    api = Namespace('book', description='book related operations')
    include_writer = api.model('include_writer', {
        'id': fields.Integer(readonly=True, description=' Writer\'s id'),
        'first_name': fields.String(required=True, description='writer first name'),
        'last_name': fields.String(required=True, description='writer last name'),
    })


class BookDto:
    api = Namespace('book', description='book related operations')
    book = api.model('book', {
        'id': fields.Integer(readonly=True, description='Book\'s id'),
        'name': fields.String(required=True, description='Book\'s name'),
        'authors': fields.List(fields.Nested(WriterIncludeDto.include_writer),
                               description='Book\'s authors'),
        'rating': fields.Integer(readonly=True, description='Book\'s rating'),
    })


class BookIncludeDto:
    api = Namespace('writers', description='writer related operations')
    include_book = api.model('include_book', {
        'id': fields.Integer(readonly=True, description='Book\'s id'),
        'name': fields.String(required=True, description='Book\'s name'),
        'rating': fields.Integer(readonly=True, description='Book\'s rating'),
    })


class WriterDto:
    api = Namespace('writers', description='writer app related operations')
    writer = api.model('writer', {
        'id': fields.Integer(readonly=True, description=' Writer\'s id'),
        'first_name': fields.String(required=True, description='writer first name'),
        'last_name': fields.String(required=True, description='writer last name'),
        # 'top_books': fields.List(fields.String)
        'top_books': fields.List(fields.Nested(BookIncludeDto.include_book),
                                 description='Writers\'s top books'),
    })


class RatingDto:
    api = Namespace('book', description='main app related operations')
    rating = api.model('rating', {
        'value': fields.Integer(description='rating value 1 - 5', min=1, max=5)
    })
