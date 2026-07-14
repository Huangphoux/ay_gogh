"""AGSI Minification Middleware build on top of Starlette.

Code is based on GZipMiddleware shipped with Starlette,
and BrotliMiddleware.

The middleware should be below any other middleware that may encode your responses,
such as Starlette’s GZipMiddleware
"""

from rcssmin import cssmin
from rjsmin import jsmin

import re
from typing import List, Union, NoReturn

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

import minify_html_onepass


class MinificationMiddleware:
    """Minification Middleware public interface."""

    def __init__(
        self,
        app: ASGIApp,
        minimum_size: int = 400,
        excluded_handlers: Union[List, None] = None,
    ) -> None:
        """
        Arguments.

        minimum_size: Only compress responses that are bigger than this value in bytes.
        excluded_handlers: List of handlers to be excluded from being compressed.
        """
        self.app = app
        self.minimum_size = minimum_size
        if excluded_handlers:
            self.excluded_handlers = [re.compile(path) for path in excluded_handlers]
        else:
            self.excluded_handlers = []

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self._is_handler_excluded(scope) or scope["type"] != "http":
            return await self.app(scope, receive, send)
        responder = MinificationResponder(self.app, self.minimum_size)
        await responder(scope, receive, send)

    def _is_handler_excluded(self, scope: Scope) -> bool:
        handler = scope.get("path", "")

        return any(pattern.search(handler) for pattern in self.excluded_handlers)


class MinificationResponder:
    """Minification Interface."""

    def __init__(self, app: ASGIApp, minimum_size: int) -> None:  # noqa
        self.app = app
        self.minimum_size = minimum_size

        self.send: Send = unattached_send  # type: Send
        self.initial_message: Message = {}  # type: Message
        self.started: bool = False

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:  # noqa
        self.send = send
        await self.app(scope, receive, self.send_minified)

    async def send_minified(self, message: Message) -> None:
        """Apply compression using brotli."""
        message_type = message["type"]

        if message_type == "http.response.start":
            # Don't send the initial message
            # until we've determined how to modify the outgoing headers correctly.
            self.initial_message = message

        elif message_type == "http.response.body" and not self.started:
            self.started = True
            body: bytes = message.get("body", b"")
            more_body: bool = message.get("more_body", False)

            if len(body) < self.minimum_size and not more_body:
                # Don't minify small outgoing responses.
                await self.send(self.initial_message)
                await self.send(message)

            elif not more_body:  # Standard response.
                headers = MutableHeaders(raw=self.initial_message["headers"])

                if "text/html" in headers["Content-Type"]:
                    body = self._process(body)
                if "text/css" in headers["Content-Type"]:
                    body = self._process(body, is_css=True)
                if "application/javascript" in headers["Content-Type"]:
                    body = self._process(body, is_js=True)

                headers["Content-Length"] = str(len(body))
                message["body"] = body

                await self.send(self.initial_message)
                await self.send(message)
            else:  # Initial body in streaming response.
                await self.send(self.initial_message)
                await self.send(message)

        elif message_type == "http.response.body":
            # Remaining body in streaming response.
            await self.send(message)
        else:
            await self.send(self.initial_message)
            await self.send(message)

    def _process(self, body: bytes, is_css=False, is_js: bool = False) -> bytes:
        if is_css:
            return cssmin(body)
        if is_js:
            return jsmin(body)

        return minify_html_onepass.minify(
            minify_css=True, minify_js=True, code=body.decode()
        ).encode()


async def unattached_send(message: Message) -> NoReturn:
    raise RuntimeError("send awaitable not set")  # pragma: no cover
