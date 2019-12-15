from flask_restplus import Api
from flask import Blueprint

from app.main.utils.dto import WriterIncludeDto, BookIncludeDto, RatingDto
from .main.controllers.user_controller import api as user_ns
from .main.controllers.auth_controller import api as auth_ns
from .main.controllers.book_controller import api as book_ns
from .main.controllers.writer_controller import api as writer_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK BOOK RATING APPLICATION API',
          version='1.0',
          description='a application for Digital Security test task'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(writer_ns, path='/writers')
api.add_namespace(book_ns, path='/books')
api.add_namespace(WriterIncludeDto.api)
api.add_namespace(BookIncludeDto.api)
api.add_namespace(RatingDto.api)
