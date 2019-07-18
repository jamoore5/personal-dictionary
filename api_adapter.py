from tornado.httpclient import AsyncHTTPClient
import json


class ApiAdapter:
    def __init__(self):
        self.http_client = AsyncHTTPClient()

    async def fetch(self, endpoint):
        response = await self.http_client.fetch("http://localhost:8888/" + endpoint)
        return json.loads(response.body.decode('utf-8'))['data']
