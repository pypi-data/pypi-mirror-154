=====
Usage
=====

To use flask-request-guid in a project::

    from flask import Flask
    from flask_request_guid import FlaskRequestGUID

    app = Flask(__name__)
    frguid = FlaskRequestGUID(app)

    @app.route("/hello"):
    def hello():
        return f"Hello from request {frguid.request_id}"
