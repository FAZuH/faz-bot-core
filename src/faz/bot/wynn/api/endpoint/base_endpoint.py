from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faz.bot.wynn.api.http_request import HttpRequest


class BaseEndpoint(ABC):
    __slots__ = ("_request", "_retries", "_retry_on_exc")

    def __init__(self, request: HttpRequest, retries: int, retry_on_exc: bool) -> None:
        self._request = request
        self._retries = retries
        self._retry_on_exc = retry_on_exc

    @property
    @abstractmethod
    def path(self) -> str: ...
