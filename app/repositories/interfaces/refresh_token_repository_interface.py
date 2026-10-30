from abc import ABC, abstractmethod
from app.models.refresh_token_model import RefreshToken

class RefreshTokenRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, token: RefreshToken) -> RefreshToken: ...
    @abstractmethod
    async def get_by_hash(self, token_hash: str) -> RefreshToken | None: ...
