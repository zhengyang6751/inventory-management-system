from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.initial_data import init_db as init_initial_data
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 307:  # Temporary Redirect
            # Remove trailing slash and return original response
            if request.url.path != "/" and request.url.path.endswith("/"):
                return RedirectResponse(
                    url=str(request.url)[:-1],
                    status_code=308  # Permanent Redirect
                )
        return response

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # Disable automatic redirect
    redirect_slashes=False
)

# Add trailing slash middleware
app.add_middleware(TrailingSlashMiddleware)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False for wildcard origins
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include API router with explicit prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Inventory Management System API",
        "docs_url": "/docs"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)  # Initialize database tables
    init_initial_data(db)  # Initialize initial data
    db.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 