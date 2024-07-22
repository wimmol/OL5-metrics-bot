from datetime import time
from typing import Callable, Dict, Any, Awaitable

import time
from aiogram import BaseMiddleware
from aiogram.types import Message

from app.calc import TokensData
from app.requests import fetchTokensData


class TokensMiddleware(BaseMiddleware):
    def setTokens(self):
        self.tokens = fetchTokensData()
        self.last_request_time = time.time()
        self.tokens_data = TokensData(self.tokens)

    def __init__(self) -> None:
        print('Middleware initialized')
        self.tokens = []
        self.last_request_time = 0
        self.tokens_data = None
        self.setTokens()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        print('Middleware work')
        if time.time() - self.last_request_time > 600:
            print('Middleware fetch')
            self.setTokens()

        return await handler(event, data)

    def get_tokens_data(self):
        return self.tokens_data
