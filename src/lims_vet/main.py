from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.database import engine
from .api.v1.reports import router as reports_router
from .api.v1.samples import router as samples_router
from .api.ws import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Cleanup on shutdown
    await engine.dispose()

app = FastAPI(title="LIMS Vet API", version="0.1.0", lifespan=lifespan)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reports_router, prefix="/api/v1")
app.include_router(samples_router, prefix="/api/v1")
app.include_router(ws_router)
