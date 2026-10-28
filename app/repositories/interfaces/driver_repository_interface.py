from abc import ABC, abstractmethod

from app.models.driver_model import Driver

#These abstract methods must have the implementation at the child class.
class DriverRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, driver: Driver) -> Driver:
        pass

    @abstractmethod
    async def get_all(self) -> list[Driver]:
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




    # @abstractmethod
    # async def get_driver_report(
    #     self,
    #     start_date: date | None = None,
    #     end_date: date | None = None,
    # ) -> list[dict[str, Any]]:
    #     pass