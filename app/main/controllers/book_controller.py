from flask import request, jsonify
from flask_restplus import Resource

from app.main.models.book import Book
from app.main.utils.decorator import add_access_token_header, token_required, admin_token_required
from ..utils.dto import BookDto, WriterDto, RatingDto
from ..services.book_service import save_new_book, get_book, add_book_rating, \
    delete_book, update_book

api = BookDto.api
_book = BookDto.book
_writer = WriterDto.writer
_rating = RatingDto.rating


@api.route('/page')
@add_access_token_header(api)
class BookList(Resource):
    @token_required
    # @api.marshal_list_with(_book, envelope='data')
    def get(self, **kwargs):
        """List all books"""
        return pagination.paginate(AuthorModel, author_fields)

    @api.expect(_book, validate=True)
    @api.response(201, 'Book successfully created.')
    @token_required
    def post(self, **kwargs):
        """Creates a new Book"""
        data = request.json
        return save_new_book(data=data)


@api.route('/<book_id>')
@api.param('book_id', 'The Book identifier')
@api.response(404, 'Book not found.')
@add_access_token_header(api)
class BookResource(Resource):
    @api.doc('get a book')
    @api.marshal_with(_book)
    @token_required
    def get(self, book_id):
        """Get a book by id"""
        book = get_book(book_id)
        if not book:
            api.abort(404)
        else:
            return book

    @api.doc('update a book')
    @api.expect(_book, validate=True)
    @api.marshal_with(_book)
    @token_required
    def patch(self, book_id):
        """Update a book by id"""
        data = request.json
        response = update_book(book_id, data)
        return response

    @api.doc('update a book')
    @api.expect(_book, validate=True)
    @api.marshal_with(_book)
    @token_required
    def put(self, book_id):
        """Update a book by id"""
        data = request.json
        response = update_book(book_id, data)
        return response

    @api.doc('delete a book')
    @api.marshal_with(_book)
    @admin_token_required
    def delete(self, book_id):
        """Delete a book by id"""
        response = delete_book(book_id)
        return response


@api.route('/<book_id>/add-rating')
@api.param('book_id', 'The Book identifier')
@add_access_token_header(api)
class BookRating(Resource):
    @api.expect(_rating, validate=True)
    @api.response(201, 'New rating for book successfully added.')
    @api.doc('add book rating')
    @token_required
    def post(self, book_id, **kwargs):
        """Add rating"""
        data = request.json
        return add_book_rating(user_id=kwargs.get('user_id'), book_id=book_id, data=data)
