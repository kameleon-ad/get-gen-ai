from flask import (
    Blueprint,
    jsonify,
)

api_contents_bp = Blueprint('contents', __name__)


@api_contents_bp.get('/status')
def status():
    return jsonify({
        "status": True,
    })
