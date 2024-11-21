from typing import Any, override

from faz.fazbot.wynn.api.base_response import BaseResponse
from faz.fazbot.wynn.api.model.guild import Guild
from faz.fazbot.wynn.api.model.headers import Headers


class GuildResponse(BaseResponse[Guild, Headers]):
    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(Guild(body), Headers(headers))

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.body.name})"
