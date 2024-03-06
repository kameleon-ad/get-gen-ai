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
from app.extensions import SQL_DB
from app.gateway import authorization_require
from app.models import Content
from app.utils import logged_input
from app.validator import (
    ContentValidation,
    ReviewValidation,
)

api_contents_bp = Blueprint('contents', __name__)


@api_contents_bp.get('/status')
def status():
    return jsonify({
        "status": True,
    })


@api_contents_bp.get('/')
def retrieve_all_contents():
    created_by = request.args.get('created_by')
    reviewed_by = request.args.get('reviewed_by')
    query = Content.query
    if created_by:
        query = query.filter(Content.created_by == created_by)
    if reviewed_by:
        query = query.filter(Content.reviewed_by == reviewed_by)
    return send_result(data=[content.raw for content in query.all()])


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


@api_contents_bp.put('/<int:content_id>')
@authorization_require()
def review_content(content_id: int, payload: dict):
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
    is_not_validate = ReviewValidation().validate(json_body)  # Dictionary show detail error fields
    if is_not_validate:
        return send_error(data=is_not_validate, message='Invalid parameters')
    
    content = Content.query.get(content_id)
    if content is None:
        return send_error(message=f'Content with the id-{content_id} not found', code=404)
    
    if content.reviewed_by:
        return send_error(message=f'Content with the id-{content_id} is already reviewed', code=422)
    
    content.review = json_body.get('review')
    content.reviewed_by = payload.get('sub')
    content.update()
    return send_result(data=content.raw, message='Successfully saved!')


@api_contents_bp.delete('/<int:content_id>')
def delete_content(content_id: int):
    content = Content.query.get(content_id)
    if content is None:
        return send_result()
    try:
        SQL_DB.session.delete(content)
        SQL_DB.session.commit()
    except:
        return send_error(message=f'Failed to delete the content with id-{content_id}')
    return send_result()
