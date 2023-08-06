#!/usr/bin/env python
"""Tests for `flask_request_guid` package."""
import uuid
from collections.abc import Iterator

import pytest
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask.testing import FlaskClient
from flask_request_guid import FlaskRequestGUID


@pytest.fixture()
def app() -> Iterator[Flask]:

    app = Flask(__name__)
    app.config.update({"TESTING": True})

    @app.route("/home/")
    def home() -> Response:
        return "Hello World!"

    @app.route("/get-request-id/")
    def get_request_id() -> Response:
        return jsonify({"request-id": getattr(request, "id", None)})

    yield app


@pytest.fixture()
def extension(app: Flask) -> FlaskRequestGUID:

    ext = FlaskRequestGUID(app)

    @app.route("/get-extension-request-id/")
    def get_request_id_extension() -> Response:
        return jsonify({"request-id": ext.request_id})

    return ext


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def request_id(monkeypatch: pytest.MonkeyPatch) -> Iterator[uuid.UUID]:
    id = uuid.uuid4()

    def mock_generate_id(self: FlaskRequestGUID) -> str:
        return str(id)

    monkeypatch.setattr(FlaskRequestGUID, "generate_id", mock_generate_id)
    yield id


def test_set_header(client: FlaskClient, extension: FlaskRequestGUID, request_id: uuid.UUID) -> None:

    response = client.get("/home/")
    assert response.status_code == 200

    id = response.headers[extension.header_name]

    assert uuid.UUID(id) == request_id


def test_explicit_header(client: FlaskClient, extension: FlaskRequestGUID, request_id: uuid.UUID) -> None:
    new_id = "not-a-uuid-id"

    response = client.get("/home/", headers={"X-Request-ID": new_id})
    assert response.status_code == 200

    id = response.headers[extension.header_name]
    assert id != str(request_id)
    assert id == new_id


def test_set_different_header(client: FlaskClient, extension: FlaskRequestGUID) -> None:
    response = client.get("/home/")
    assert response.status_code == 200
    first_id = response.headers[extension.header_name]

    response = client.get("/home/")
    assert response.status_code == 200
    second_id = response.headers[extension.header_name]

    assert first_id != second_id


def test_not_enabled(client: FlaskClient, app: Flask) -> None:
    app.config.update({"REQUEST_GUID_ENABLE": False})
    ext = FlaskRequestGUID()
    ext.init_app(app)

    response = client.get("/get-request-id/")
    assert response.status_code == 200
    assert ext.header_name not in response.headers
    assert response.json is not None
    assert response.json["request-id"] is None


def test_get_id_from_request(client: FlaskClient, extension: FlaskRequestGUID, request_id: uuid.UUID) -> None:

    response = client.get("/get-request-id/")
    assert response.status_code == 200
    assert response.headers[extension.header_name] == str(request_id)
    assert response.json is not None
    assert response.json["request-id"] == str(request_id)


def test_get_id_from_extension(client: FlaskClient, extension: FlaskRequestGUID, request_id: uuid.UUID) -> None:

    response = client.get("/get-extension-request-id/")
    assert response.status_code == 200
    assert response.headers[extension.header_name] == str(request_id)
    assert response.json is not None
    assert response.json["request-id"] == str(request_id)
