from flask import request
from flask_restplus import Resource

from app.main.services.pagination_helper import PAGINATION_REQUEST_PARSER
from app.main.services.writer_service import get_writers_by_page, save_new_writer, get_writer, update_writer, \
    delete_writer
from app.main.utils.decorator import add_access_token_header, token_required, admin_token_required
from app.main.utils.dto import WriterDto

api = WriterDto.api
_writer = WriterDto.writer


@api.route('/')
@add_access_token_header(api)
class WriterList(Resource):
    @token_required
    @api.param('page_num', 'The page number', required=True)
    @api.expect(PAGINATION_REQUEST_PARSER)
    def get(self, *args, **kwargs):
        """List all writers"""
        args = PAGINATION_REQUEST_PARSER.parse_args()
        page_num = args.get('page_num', 1)
        return get_writers_by_page(api, _writer, page_num, request.base_url)

    @api.expect(_writer, validate=True)
    @api.response(201, 'Writer successfully created.')
    @token_required
    def post(self, **kwargs):
        """Creates a new Writer"""
        data = request.json
        return save_new_writer(data=data)


@api.route('/<writer_id>')
@api.param('writer_id', 'The Writer identifier')
@api.response(404, 'Writer not found.')
@add_access_token_header(api)
class WriterResource(Resource):
    @api.doc('get a writer')
    @api.marshal_with(_writer)
    @token_required
    def get(self, writer_id, **kwargs):
        """Get a writer by id"""
        writer = get_writer(writer_id)
        if not writer:
            api.abort(404)
        else:
            return writer

    @api.doc('update a writer')
    @api.response(204, 'Writer successfully updated.')
    @api.expect(_writer, validate=True)
    @api.marshal_with(_writer)
    @token_required
    def patch(self, writer_id, **kwargs):
        """Update a writer by id"""
        data = request.json
        response = update_writer(writer_id, data)
        return response

    @api.doc('update a writer')
    @api.response(204, 'Writer successfully updated.')
    @api.expect(_writer, validate=True)
    @api.marshal_with(_writer)
    @token_required
    def put(self, writer_id, **kwargs):
        """Update a writer by id"""
        data = request.json
        response = update_writer(writer_id, data)
        return response

    @api.doc('delete a writer')
    @api.marshal_with(_writer)
    @admin_token_required
    def delete(self, writer_id):
        """Delete a writer by id"""
        response = delete_writer(writer_id)
        return response
