from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import traceback
from app.api.v1.routes import auth, tenants, public_intake

logger = logging.getLogger("uvicorn.access")
app = FastAPI(
    title="Multi-tenant Quote App API",
    version="0.1.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        logger.info(f"REQUEST: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"RESPONSE: {response.status_code}")
        return response
    except Exception as exc:
        tb = traceback.format_exc()
        logger.error(f"ERROR processing request: {request.method} {request.url}\n{tb}")
        raise exc

app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["tenants"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(public_intake.router, prefix="/api/v1/public", tags=["public"])
