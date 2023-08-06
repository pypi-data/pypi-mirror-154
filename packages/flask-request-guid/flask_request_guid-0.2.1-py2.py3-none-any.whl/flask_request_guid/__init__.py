"""Top-level package for flask-request-guid."""

__author__ = """Alex Rudy"""
__email__ = "opensource@alexrudy.net"
__version__ = "0.2.1"

import uuid

from typing import Optional
from flask import Flask, request, Response, _app_ctx_stack

__all__ = ["FlaskRequestGUID"]


class FlaskRequestGUID:
    """
    A flask extension to add a unique ID to each request.
    """

    def __init__(self, app: Optional[Flask] = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize the extension with a flask app"""
        self.app = app

        enabled = app.config.setdefault("REQUEST_GUID_ENABLE", True)
        app.config.setdefault("REQUEST_GUID_HEADER", "X-Request-ID")

        if enabled:
            app.before_request(self.start_request)
            app.after_request(self.finish_request)

    @property
    def header_name(self) -> str:
        """The name of the request ID header"""
        return self.app.config["REQUEST_GUID_HEADER"]

    @property
    def request_id(self) -> str:
        """The current request ID"""
        return _app_ctx_stack.top.request_guid

    def generate_id(self) -> str:
        """Generate a new request ID"""
        return str(uuid.uuid4())

    def start_request(self) -> None:
        """
        Start the request by getting the request ID from the reqeust headers or setting one.

        This method is internally connected to the flask :meth:`~Flask.before_request` method.
        """
        request_id = request.headers.get(self.header_name, None)
        if request_id is None:
            request_id = self.generate_id()
        request.id = request_id  # type: ignore[attr-defined]
        _app_ctx_stack.top.request_guid = request_id

    def finish_request(self, response: Response) -> Response:
        """
        Finish the request by adding the request ID to the response headers.

        This method is internally connected to the flask :meth:`~Flask.after_request` method,
        and must return the appropriate response after modifying it.
        """
        response.headers.setdefault(self.header_name, _app_ctx_stack.top.request_guid)
        return response
