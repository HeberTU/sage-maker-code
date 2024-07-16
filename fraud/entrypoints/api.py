"""API entrypoint."""
from fastapi import FastAPI

from fraud.entrypoints.routes import get_router


def get_app() -> FastAPI:
    """Get API."""
    app = FastAPI()
    app.include_router(get_router())
    return app
