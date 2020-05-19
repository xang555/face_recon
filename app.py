#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from routers import *
from werkzeug.exceptions import HTTPException
import flask_cors
import appconfig as conf

app = Flask(__name__)

# Cross Origin Resource
flask_cors.CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# upload file config
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# JWT Config
app.config['JWT_SECRET_KEY'] = "hcoirie83748374834"
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
app.config['JWT_QUERY_STRING_NAME'] = 'token'
jwt = JWTManager(app)

# register Routers
url_api_prefix = conf.api_url_prefix
app.register_blueprint(users.users, url_prefix=url_api_prefix)
app.register_blueprint(monitor.monitor, url_prefix=url_api_prefix + "/monitor")
app.register_blueprint(camera.camera, url_prefix=url_api_prefix + '/camera')
app.register_blueprint(knowPeople.know_people, url_prefix=url_api_prefix + '/know')
app.register_blueprint(access.access, url_prefix=url_api_prefix + '/access')


@app.errorhandler(HTTPException)
def handle_error(e):
    return jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }), e.code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=conf.api_server.get('port', 8080), debug=conf.api_server.get('debug', False),
            use_reloader=False, threaded=False)
