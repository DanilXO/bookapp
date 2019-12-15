from flask_restplus import reqparse

PAGINATION_LIMIT = 2
PAGINATION_REQUEST_PARSER = reqparse.RequestParser()
PAGINATION_REQUEST_PARSER.add_argument('page_num', type=int, help='The page number')


def get_paginated_list(api, marshal_object, model, page_num, base_url,
                       envelop='data', limit=PAGINATION_LIMIT):
    assert page_num >= 1, "Incorrect page num"
    data = model.query.paginate(page_num, limit, False).items
    next_data = model.query.paginate(page_num + 1, limit, False).items
    marshaled_data = api.marshal(fields=marshal_object, data=data)
    return {
        "prev": f"{base_url}?page_num={page_num - 1}" if page_num > 1 else None,
        "next": f"{base_url}?page_num={page_num + 1}" if next_data else None,
        "count": len(data),
        envelop: marshaled_data
    }
