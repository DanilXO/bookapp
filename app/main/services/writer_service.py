from app.main.models.book import Writer
from app.main.services.pagination_helper import get_paginated_list


def get_writers_by_page(api, marshal_object, page_num, base_url):
    return get_paginated_list(api, marshal_object, Writer, page_num, base_url)

def get_writer(writer_id):
    # return Writer.query.filter_by(id=writer_id).first()
    pass

def delete_writer(writer_id):
    # writer = Writer.query.filter_by(id=writer_id).first()
    # if writer:
    #     db.session.delete(writer)
    #     db.session.commit()
    #     response_object = {
    #         'status': 'success',
    #         'message': 'Writer successfully deleted.',
    #     }
    #     return response_object, 204
    # else:
    #     response_object = {
    #         'status': 'fail',
    #         'message': 'Writer does not exists.',
    #     }
    #     return response_object, 404
    pass


def update_writer(writer_id, data):
    # writer = Writer.query.filter_by(id=writer_id).first()
    # if writer:
    #     if data:
    #         authors_data = data.get('authors')
    #         if authors_data:
    #             authors = []
    #             for author_data in authors_data:
    #                 author = get_or_create(db, Writer, first_name=author_data.get('first_name'),
    #                                        last_name=author_data.get('last_name'))
    #                 authors.append(author)
    #             writer.authors = authors
    #         new_name = data.get('name')
    #         if new_name:
    #             writer.name = new_name
    #         save_changes(writer)
    #     response_object = {
    #         'status': 'success',
    #         'message': 'Writer successfully updated.',
    #     }
    #     return response_object, 204
    # else:
    #     response_object = {
    #         'status': 'fail',
    #         'message': 'Writer does not exists.',
    #     }
    #     return response_object, 404
    pass


def add_writer_rating(user_id, writer_id, data):
    # rating_exists = Rating.query.filter_by(user_id=user_id, writer_id=writer_id).first()
    # value = data['value']
    # writer = Writer.query.filter_by(id=writer_id).first()
    # user = User.query.filter_by(id=user_id).first()
    # if not writer or not user:
    #     response_object = {
    #         'status': 'fail',
    #         'message': 'Writer or user does not exists.',
    #     }
    #     return response_object, 404
    # else:
    #     if not rating_exists:
    #         new_rating = Rating(
    #             user_id=user.id,
    #             writer_id=writer.id,
    #             value=value
    #         )
    #         save_changes(new_rating)
    #     else:
    #         rating_exists.value = value
    #         save_changes(rating_exists)
    #     response_object = {
    #         'status': 'success',
    #         'message': 'New rating for writer successfully added.',
    #     }
    #     return response_object, 201
    pass


def save_new_writer(data):
    # writer_exists = Writer.query.filter_by(name=data['name']).first()
    # if not writer_exists:
    #     authors_data = data['authors']
    #     authors = []
    #     for author_data in authors_data:
    #         author = get_or_create(db, Writer, first_name=author_data.get('first_name'),
    #                                last_name=author_data.get('last_name'))
    #         authors.append(author)
    #     new_writer = Writer(
    #         name=data['name'],
    #         authors=authors
    #     )
    #     save_changes(new_writer)
    #     response_object = {
    #         'status': 'success',
    #         'message': 'Writer successfully created.',
    #     }
    #     return response_object, 201
    # else:
    #     response_object = {
    #         'status': 'fail',
    #         'message': 'Writer already exists. Please try other name.',
    #     }
    #     return response_object, 409
    pass
