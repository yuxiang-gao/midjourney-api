from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from loguru import logger

import midjourney_api.api.routes as routes
from midjourney_api.settings import settings
from midjourney_api.version import __version__

app = FastAPI(title="Midjourney", version=__version__, root_path=settings.fastapi_root_path, lifespan=routes.lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect_to_doc() -> RedirectResponse:
    return RedirectResponse(url=settings.fastapi_root_path + "/docs")


app.include_router(routes.router)
