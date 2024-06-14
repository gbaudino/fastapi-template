"""Main module to run the application."""
from contextlib import asynccontextmanager
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from configs import Settings

try:
    settings = Settings()
except:
    print("Error loading settings. Check the existence and format of the settings file.")
    sys.exit(1)

@asynccontextmanager
async def lifespan(application: FastAPI):
    """Context manager to start and stop the application."""
    try:
        yield
    finally:
        pass

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def go_to_docs():
    """Redirects the user to the API swagger documentation."""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, reload=settings.debug, port=settings.port)
