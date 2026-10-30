from abc import ABC, abstractmethod

from app.models.driver_model import Driver

#These abstract methods must have the implementation at the child class.
class DriverRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, driver: Driver) -> Driver:
        pass

    @abstractmethod
    async def get_all(self, skip: int=0, limit: int=10) -> list[Driver]:
        pass

    @abstractmethod
    async def get_by_id(self, driver_id: int) -> Driver | None:
        pass

    @abstractmethod
    async def get_with_collections(self, driver_id: int) -> Driver | None:
        pass

    @abstractmethod
    async def update(
        self, driver_id: int, changes: dict
    ) -> Driver|None:
        pass


    @abstractmethod
    async def delete_driver_using_procedure(
        self, driver_id: int
    ) -> None:
        pass

    # @abstractmethod
    # async def delete(
    #     self ,driver_id : int 
    # )-> Driver | None:
    #     pass

