
from fastapi import APIRouter, Depends, status

from app.api.dependencies.database import get_database
from app.schemas.transport_collection_schema import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
    CollectionListResponse
)
from app.services.transport_collection_service import (
    TransportCollectionService,
)
from app.api.dependencies.service_dependencies import get_collection_service

from app.api.dependencies.auth_dependencies import require_roles

from datetime import date
from fastapi import Query

router = APIRouter(
    prefix="/api/collections",
    tags=["Transport Collections"],
)


@router.post(
    "/",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin","driver"))],
)
async def add_collection(
    data: CollectionCreate,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return await service.create_collection(data)


@router.get(
    "/",
    response_model=CollectionListResponse,
    dependencies=[Depends(require_roles("admin", "driver"))],
)
async def list_collections(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    driver_id: int | None = Query(None, gt=0),
    start_date: date | None = None,
    end_date: date | None = None,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
) -> CollectionListResponse:

    return await service.get_collections(
        page=page,
        limit=limit,
        driver_id=driver_id,
        start_date=start_date,
        end_date=end_date,
    )




@router.get(
    "/{collection_id}",
    response_model=CollectionResponse,
    dependencies=[Depends(require_roles("admin","driver"))],
)
async def read_collection(
    collection_id: int,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return await service.get_collection(collection_id)


@router.patch(
    "/{collection_id}",
    response_model=CollectionResponse,
    dependencies=[Depends(require_roles("admin","driver"))],

)
async def edit_collection(
    collection_id: int,
    data: CollectionUpdate,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return await service.update_collection(
        collection_id,
        data.model_dump(exclude_unset=True),
    )


@router.delete("/{collection_id}",
                dependencies=[Depends(require_roles("driver"))],
)
async def remove_collection(
    collection_id: int,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return await service.delete_collection(collection_id)
