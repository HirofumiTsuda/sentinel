from fastapi import APIRouter, FastAPI

from app.api.v1.routers import charters, projects, stories, tasks

app = FastAPI(title="sentinel")

# All resource endpoints live under /api/v1. Not needed for sentinel's own
# frontend today (it's always deployed in lockstep), but it's free to add
# now and cheap insurance if the API ever gets a second/external consumer.
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(projects.router)
api_v1.include_router(charters.router)
api_v1.include_router(stories.router)
api_v1.include_router(tasks.router)

app.include_router(api_v1)


# Infra health check convention: intentionally unversioned.
@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
