from fastapi import APIRouter, Depends, status
from app.schemas.driver_schema import (
    DriverCreate,
    DriverResponse,
    DriverUpdate,
    DriverPatch,
    DriverWithCollectionsResponse,
)
from app.services.driver_service import DriverService

from app.api.dependencies.service_dependencies import get_driver_service


from app.api.dependencies.auth_dependencies import require_roles

router = APIRouter( 
    prefix="/api/drivers",
    tags=["Drivers"],
)


@router.post(
    "/",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
            Depends(require_roles("admin"))
        ],
)
async def add_driver(
    data: DriverCreate,
    service: DriverService = Depends(get_driver_service),
)->DriverResponse:
    return await service.create_driver(data)


@router.get("/", 
            response_model=list[DriverResponse],
            dependencies=[
                Depends(require_roles("admin","driver"))
            ],
            )
async def list_drivers(
    service: DriverService = Depends(get_driver_service),
)->list[DriverResponse]:
    return await service.get_drivers()


# router to get driver with collection 
@router.get(
    "/{driver_id}/collections",
    response_model=DriverWithCollectionsResponse,
    dependencies=[Depends(require_roles("admin","driver"))]
)
async def read_driver_with_collections(
    driver_id: int,
    service: DriverService = Depends(get_driver_service),
):
    return await service.get_driver_with_collection(driver_id)


# router to get driver with id 
@router.get(
    "/{driver_id}",
    response_model=DriverResponse,
    dependencies=[Depends(require_roles("admin","driver"))]
)
async def read_driver(
    driver_id: int,
    service: DriverService = Depends(get_driver_service),
):
    return await service.get_driver(driver_id)


#must specify all the fields
@router.put("/{driver_id}", 
            response_model=DriverResponse,
            dependencies=[Depends(require_roles("admin"))]
            )
async def replace_driver(
    driver_id: int,
    data: DriverUpdate,
    service: DriverService = Depends(get_driver_service),
) -> DriverResponse:
    return await service.update_driver(
        driver_id, data.model_dump()
    )

# Can update only the required fields
@router.patch("/{driver_id}", 
        response_model=DriverResponse, 
        dependencies=[Depends(require_roles("admin"))]
        )
async def patch_driver(
    driver_id: int,
    data: DriverPatch,
    service: DriverService = Depends(get_driver_service),
) -> DriverResponse:
    return await service.update_driver(
        driver_id,
        data.model_dump(exclude_unset=True),
    )


@router.delete(
    "/{driver_id}",
    dependencies=[Depends(require_roles("admin"))]
    
)
async def remove_driver(
    driver_id: int,
    service: DriverService = Depends(get_driver_service),
):
    await service.delete_driver(driver_id)

    return {
        "message" : "Driver deleted successfully",
        "driver_id":  driver_id
    }   
