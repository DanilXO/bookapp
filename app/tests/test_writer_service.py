import unittest

from app.main import db
from app.main.models.book import Writer
from app.main.services.writer_service import get_writer, delete_writer, update_writer, save_new_writer
from app.tests.base import BaseTestCase


class TestWriterService(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.writer = Writer(
            first_name='Test',
            last_name='Test'
        )
        db.session.add(self.writer)
        db.session.commit()

    def test_get_writer(self):
        writer_from_db = get_writer(self.writer.id)
        self.assertEqual(self.writer, writer_from_db)

    def test_delete_writer(self):
        writer_for_delete = Writer(
            first_name='TestForDelete',
            last_name='TestForDelete'
        )
        db.session.add(writer_for_delete)
        db.session.commit()
        deleted_writer_id = writer_for_delete.id
        success_response_object = {
            'status': 'success',
            'message': 'Writer successfully deleted.',
        }
        fail_response_object = {
            'status': 'fail',
            'message': 'Writer does not exists.',
        }
        response_object, code = delete_writer(deleted_writer_id)
        self.assertEqual(response_object, success_response_object)
        self.assertEqual(code, 204)
        response_object, code = delete_writer(9999)
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 404)

    def test_update_writer(self):
        new_authors_data = {'first_name': 'Jack', 'last_name': 'Palanik'}
        success_response_object = {
            'status': 'success',
            'message': 'Writer successfully updated.',
        }
        fail_response_object = {
            'status': 'fail',
            'message': 'Writer does not exists.',
        }
        response_object, code = update_writer(self.writer.id, new_authors_data)
        self.assertEqual(response_object, success_response_object)
        self.assertEqual(code, 204)
        self.assertEqual(self.writer.first_name, new_authors_data.get('first_name'))
        self.assertEqual(self.writer.last_name, new_authors_data.get('last_name'))
        prev_first_name = self.writer.first_name
        prev_last_name = self.writer.last_name
        response_object, code = update_writer(999, new_authors_data)
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 404)
        self.assertEqual(self.writer.first_name, prev_first_name)
        self.assertEqual(self.writer.last_name, prev_last_name)

    def test_save_new_writer(self):
        new_writer_data = {
            'first_name': 'New',
            'last_name': 'Author'
        }
        success_response_object = {
            'status': 'success',
            'message': 'Writer successfully created.',
        }
        fail_response_object = {
            'status': 'fail',
            'message': 'Writer already exists. Please try other name.',
        }
        response_object, code = save_new_writer(new_writer_data)
        self.assertEqual(response_object, success_response_object)
        self.assertEqual(code, 201)
        response_object, code = save_new_writer({'first_name': self.writer.first_name,
                                                 'last_name': self.writer.last_name})
        self.assertEqual(response_object, fail_response_object)
        self.assertEqual(code, 409)


if __name__ == '__main__':
    unittest.main()
