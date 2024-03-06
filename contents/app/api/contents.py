import json

from flask import (
    Blueprint,
    jsonify,
    request,
)

from app.api.helper import (
    send_error,
    send_result,
)
from app.gateway import authorization_require
from app.models import Content
from app.utils import logged_input
from app.validator import ContentValidation

api_contents_bp = Blueprint('contents', __name__)


@api_contents_bp.get('/status')
def status():
    return jsonify({
        "status": True,
    })


@api_contents_bp.get('/')
def retrieve_all_contents():
    return send_result(data=Content.retrieve_all())


@api_contents_bp.get('/<int:content_id>')
def retrieve_content_by_id(content_id):
    content = Content.query.get(content_id)
    if content is None:
        return send_error(message=f'Content with the id-{content_id} not found', code=404)
    return send_result(data=content.raw)


@api_contents_bp.post('/')
@authorization_require()
def create_content(payload: dict):
    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message='Request Body incorrect json format: ' + str(ex), code=442)

    # Log request api
    logged_input(json.dumps(json_req))
    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    # validate request body
    is_not_validate = ContentValidation().validate(json_body)  # Dictionary show detail error fields
    if is_not_validate:
        return send_error(data=is_not_validate, message='Invalid parameters')

    title = json_body.get('title')
    content_str = json_body.get('content')
    user_id = payload.get('sub')
    new_content = Content.create(title=title, content=content_str, created_by=user_id)

    return send_result(data=new_content.raw)
