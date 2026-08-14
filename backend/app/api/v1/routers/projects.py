import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.db.session import get_db
from app.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


async def get_project_or_404(project_id: uuid.UUID, db: AsyncSession) -> Project:
    project = await db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(db: AsyncSession = Depends(get_db)) -> list[Project]:
    result = await db.execute(select(Project).order_by(Project.created_at))
    return list(result.scalars().all())


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate, db: AsyncSession = Depends(get_db)
) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Project:
    return await get_project_or_404(project_id, db)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: uuid.UUID, payload: ProjectUpdate, db: AsyncSession = Depends(get_db)
) -> Project:
    project = await get_project_or_404(project_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    project = await get_project_or_404(project_id, db)
    await db.delete(project)
    await db.commit()
