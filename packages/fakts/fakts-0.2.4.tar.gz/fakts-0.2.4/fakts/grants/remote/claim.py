import asyncio
from typing import Optional
from urllib.parse import urlencode
import uuid
import webbrowser
from pydantic import Field
import requests
from fakts.grants.remote.base import RemoteGrant


class ClaimGrant(RemoteGrant):
    client_id: str
    client_secret: str
    graph: Optional[str]
    version: Optional[str]

    async def aload(self):

        endpoint = await self.discovery.discover()

        answer = requests.post(
            f"{endpoint.base_url}claim/",
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "graph": self.graph,
                "version": self.version,
                "scopes": self.scopes,
            },
        )

        if answer.status_code == 200:
            nana = answer.json()
            return nana["config"]
        else:
            raise Exception("Error! Coud not claim this app on this endpoint")
