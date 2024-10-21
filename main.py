from contextlib import asynccontextmanager
from fastapi import FastAPI
from logger import logger
from database import create_table, delete_table
from src.auth.router import router as user_router
from src.candidates.router import router_profile as candidates_router
from src.candidates.router import router_skill as candidate_skill_router
from src.recruiters.router import router_profile as recruiters_router
from src.matching.router import router as matching_router
from src.jobs.router import router_job as jobs_router
from src.jobs.router import router_req as job_req_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    logger.info("Starting application, initializing database.")
    yield
    # await delete_table()
    logger.info("App stopped.")

app = FastAPI(lifespan=lifespan)

app.include_router(candidates_router, prefix='/api/v1')
app.include_router(candidate_skill_router, prefix='/api/v1')
app.include_router(recruiters_router, prefix='/api/v1')
app.include_router(matching_router, prefix='/api/v1')
app.include_router(jobs_router, prefix='/api/v1')
app.include_router(job_req_router, prefix='/api/v1')
app.include_router(user_router, prefix='/api/v1')
