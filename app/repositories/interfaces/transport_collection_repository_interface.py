from abc import ABC, abstractmethod

from app.models.transport_collection_model import TransportCollection


class TransportCollectionRepositoryInterface(ABC):

    @abstractmethod
    async def create(
        self, collection: TransportCollection
    ) -> TransportCollection:
        pass

    @abstractmethod
    async def get_all(self, skip: int=0, limit: int=10) -> list[TransportCollection]:
        pass

    @abstractmethod
    async def get_by_id(
        self, collection_id: int
    ) -> TransportCollection | None:
        pass

    @abstractmethod
    async def update_collection(
        self,
        collection: TransportCollection,
        update_data: dict,
    ) -> TransportCollection:
        pass

    @abstractmethod
    async def delete(self, collection: TransportCollection) -> None:
        pass