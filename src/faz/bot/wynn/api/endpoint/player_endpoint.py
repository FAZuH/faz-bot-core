from __future__ import annotations

from typing import TYPE_CHECKING

from faz.bot.wynn.api.endpoint.base_endpoint import BaseEndpoint
from faz.bot.wynn.api.response.online_players_response import OnlinePlayersResponse
from faz.bot.wynn.api.response.player_response import PlayerResponse

if TYPE_CHECKING:
    from uuid import UUID


class PlayerEndpoint(BaseEndpoint):
    async def get_full_stats(self, username_or_uuid: str | UUID) -> PlayerResponse:
        response = await self._request.get(
            f"{self.path}/%s?fullResult=True" % username_or_uuid,
            retries=self._retries,
            retry_on_exc=self._retry_on_exc,
        )
        return PlayerResponse(response.body, response.headers)

    async def get_online_uuids(self) -> OnlinePlayersResponse:
        response = await self._request.get(
            f"{self.path}?identifier=uuid",
            retries=self._retries,
            retry_on_exc=self._retry_on_exc,
        )
        return OnlinePlayersResponse(response.body, response.headers)

    @property
    def path(self) -> str:
        return "/v3/player"
