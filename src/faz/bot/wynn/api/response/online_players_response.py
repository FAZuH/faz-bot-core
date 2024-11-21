from typing import Any

from faz.bot.wynn.api.base_response import BaseResponse
from faz.bot.wynn.api.model.headers import Headers
from faz.bot.wynn.api.model.online_players import OnlinePlayers


class OnlinePlayersResponse(BaseResponse[OnlinePlayers, Headers]):
    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(OnlinePlayers(body), Headers(headers))
