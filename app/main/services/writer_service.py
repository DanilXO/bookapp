from app.main import db
from app.main.models.book import Writer
from app.main.services.pagination_helper import get_paginated_list
from app.main.services.user_service import save_changes


def get_writers_by_page(api, marshal_object, page_num, base_url):
    return get_paginated_list(api, marshal_object, Writer, page_num, base_url)


def save_new_writer(data):
    writer_exists = Writer.query.filter_by(first_name=data['first_name'],
                                           last_name=data['last_name']).first()
    if not writer_exists:
        new_writer = Writer(
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        save_changes(new_writer)
        response_object = {
            'status': 'success',
            'message': 'Writer successfully created.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Writer already exists. Please try other name.',
        }
        return response_object, 409


def get_writer(writer_id):
    return Writer.query.filter_by(id=writer_id).first()


def delete_writer(writer_id):
    writer = Writer.query.filter_by(id=writer_id).first()
    if writer:
        db.session.delete(writer)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Writer successfully deleted.',
        }
        return response_object, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'Writer does not exists.',
        }
        return response_object, 404


def update_writer(writer_id, data):
    writer = Writer.query.filter_by(id=writer_id).first()
    if writer:
        if data:
            new_name_first_name = data.get('first_name')
            new_name_last_name = data.get('last_name')
            if new_name_first_name:
                writer.first_name = new_name_first_name
            if new_name_last_name:
                writer.last_name = new_name_last_name
            save_changes(writer)
        response_object = {
            'status': 'success',
            'message': 'Writer successfully updated.',
        }
        return response_object, 204
    else:
        response_object = {
            'status': 'fail',
            'message': 'Writer does not exists.',
        }
        return response_object, 404

