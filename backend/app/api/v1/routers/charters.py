import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers.projects import get_project_or_404
from app.api.v1.schemas.charter import CharterCreate, CharterRead, CharterUpdate
from app.db.session import get_db
from app.models import Charter

router = APIRouter(tags=["charters"])


async def get_charter_or_404(charter_id: uuid.UUID, db: AsyncSession) -> Charter:
    charter = await db.get(Charter, charter_id)
    if charter is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charter not found")
    return charter


@router.get("/projects/{project_id}/charters", response_model=list[CharterRead])
async def list_charters(
    project_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[Charter]:
    await get_project_or_404(project_id, db)
    result = await db.execute(
        select(Charter).where(Charter.project_id == project_id).order_by(Charter.created_at)
    )
    return list(result.scalars().all())


@router.post(
    "/projects/{project_id}/charters",
    response_model=CharterRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_charter(
    project_id: uuid.UUID, payload: CharterCreate, db: AsyncSession = Depends(get_db)
) -> Charter:
    await get_project_or_404(project_id, db)
    charter = Charter(**payload.model_dump(), project_id=project_id)
    db.add(charter)
    await db.commit()
    await db.refresh(charter)
    return charter


@router.get("/charters/{charter_id}", response_model=CharterRead)
async def get_charter(
    charter_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Charter:
    return await get_charter_or_404(charter_id, db)


@router.patch("/charters/{charter_id}", response_model=CharterRead)
async def update_charter(
    charter_id: uuid.UUID, payload: CharterUpdate, db: AsyncSession = Depends(get_db)
) -> Charter:
    charter = await get_charter_or_404(charter_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(charter, field, value)
    await db.commit()
    await db.refresh(charter)
    return charter


@router.delete("/charters/{charter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_charter(charter_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    charter = await get_charter_or_404(charter_id, db)
    await db.delete(charter)
    await db.commit()
