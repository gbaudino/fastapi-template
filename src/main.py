"""Main module to run the application."""
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from configs import Settings

try:
    settings = Settings()
except ValidationError:
    print('Error loading settings. Check the existence and format of the settings file.')
    sys.exit(1)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Context manager to start and stop the application."""
    try:
        # Set up your databases and resources here.
        yield
    finally:
        pass

app = FastAPI(
    title=settings.app_name,
    description=settings.app_summary,
    version=settings.app_version,
    lifespan=lifespan,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', tags=['Root'])
def go_to_docs():
    """Redirects the user to the API swagger documentation."""
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.host,
                reload=settings.debug, port=settings.port)
