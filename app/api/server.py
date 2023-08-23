from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from loguru import logger

import app.api.routes as routes
from app.settings import settings
from app.version import __version__

app = FastAPI(title="Moderato", version=__version__, root_path=settings.fastapi_root_path, lifespan=routes.lifespan)


@app.get("/")
async def redirect_to_doc() -> RedirectResponse:
    return RedirectResponse(url=settings.fastapi_root_path + "/docs")


app.include_router(routes.router)
