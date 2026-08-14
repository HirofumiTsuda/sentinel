import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers.stories import get_story_or_404
from app.api.v1.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.db.session import get_db
from app.models import Task

router = APIRouter(tags=["tasks"])


async def get_task_or_404(task_id: uuid.UUID, db: AsyncSession) -> Task:
    task = await db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("/stories/{story_id}/tasks", response_model=list[TaskRead])
async def list_tasks(story_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[Task]:
    await get_story_or_404(story_id, db)
    result = await db.execute(
        select(Task).where(Task.story_id == story_id).order_by(Task.created_at)
    )
    return list(result.scalars().all())


@router.post(
    "/stories/{story_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    story_id: uuid.UUID, payload: TaskCreate, db: AsyncSession = Depends(get_db)
) -> Task:
    await get_story_or_404(story_id, db)
    task = Task(**payload.model_dump(), story_id=story_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Task:
    return await get_task_or_404(task_id, db)


@router.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: uuid.UUID, payload: TaskUpdate, db: AsyncSession = Depends(get_db)
) -> Task:
    task = await get_task_or_404(task_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    task = await get_task_or_404(task_id, db)
    await db.delete(task)
    await db.commit()
