from flask import Flask
from flask_cors import CORS
from flask_jwt_extended.jwt_manager import JWTManager
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from api.routes import create_route

config = {
    'JSON_SORT_KEYS': False,
    'MONGODB_SETTINGS': {
        'host': 'mongodb://localhost/schools'
    },
    'JWT_SECRET_KEY': '&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdSg',
    'JWT_ACCESS_TOKEN_EXPIRES': 300,
    'JWT_REFRESH_TOKEN_EXPIRES': 604800
}

# init flask
app = Flask(__name__)

# configure app
app.config.update(config)

# init api and routes
api = Api(app)
create_route(api=api)

# init mongoengine
db = MongoEngine(app=app)

# init jwt manager
jwt = JWTManager(app=app)

# setup CORS
CORS(app, resources={r"/*": {"origin": "*"}})

# swagger specific
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Flask RESTful API"
    }
)
app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
