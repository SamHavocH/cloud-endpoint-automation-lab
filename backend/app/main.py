from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.database import SessionLocal
from app.routes import automations, compliance, devices, health
from app.seed import init_db, seed_devices


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    with SessionLocal() as db:
        seed_devices(db)
    yield


app = FastAPI(
    title="Cloud Endpoint Automation Lab API",
    description="Local demo API for endpoint inventory, compliance, and automation workflows.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(devices.router)
app.include_router(compliance.router)
app.include_router(automations.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: object, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: object, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Request validation failed.",
            "details": exc.errors(),
        },
    )
