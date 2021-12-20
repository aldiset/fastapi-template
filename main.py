from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from uvicorn import run

from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.src.router.api import router
from app.src.router.root.api import router as root_router
from app.src.database.engine import Base
from app.src.core import config

def app():
    application = FastAPI(
        title=config.PROJECT_NAME,
        docs_url=f"{config.API_PREFIX}/docs",
        openapi_url=f"{config.API_PREFIX}/openapi.json"
    )
    application.include_router(router, prefix=config.API_PREFIX)
    application.include_router(root_router, tags=["root"], prefix="")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # application.add_exception_handler(HTTPException)
    # application.add_exception_handler(RequestValidationError)

    return application

app = app()

if __name__ == '__main__':
    run(app=app)