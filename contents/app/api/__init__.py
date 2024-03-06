from flask import Blueprint

from app.api.contents import api_contents_bp

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(api_contents_bp, url_prefix='/contents')
