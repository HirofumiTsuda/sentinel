import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers.charters import get_charter_or_404
from app.api.v1.schemas.story import StoryCreate, StoryRead, StoryUpdate
from app.db.session import get_db
from app.models import Story

router = APIRouter(tags=["stories"])


async def get_story_or_404(story_id: uuid.UUID, db: AsyncSession) -> Story:
    story = await db.get(Story, story_id)
    if story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    return story


@router.get("/charters/{charter_id}/stories", response_model=list[StoryRead])
async def list_stories(
    charter_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[Story]:
    await get_charter_or_404(charter_id, db)
    result = await db.execute(
        select(Story).where(Story.charter_id == charter_id).order_by(Story.created_at)
    )
    return list(result.scalars().all())


@router.post(
    "/charters/{charter_id}/stories",
    response_model=StoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_story(
    charter_id: uuid.UUID, payload: StoryCreate, db: AsyncSession = Depends(get_db)
) -> Story:
    await get_charter_or_404(charter_id, db)
    story = Story(**payload.model_dump(), charter_id=charter_id)
    db.add(story)
    await db.commit()
    await db.refresh(story)
    return story


@router.get("/stories/{story_id}", response_model=StoryRead)
async def get_story(story_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Story:
    return await get_story_or_404(story_id, db)


@router.patch("/stories/{story_id}", response_model=StoryRead)
async def update_story(
    story_id: uuid.UUID, payload: StoryUpdate, db: AsyncSession = Depends(get_db)
) -> Story:
    story = await get_story_or_404(story_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(story, field, value)
    await db.commit()
    await db.refresh(story)
    return story


@router.delete("/stories/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(story_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    story = await get_story_or_404(story_id, db)
    await db.delete(story)
    await db.commit()
