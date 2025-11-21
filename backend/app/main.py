from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import auth, tenants, public_intake

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

app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["tenants"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(public_intake.router, prefix="/api/v1/public", tags=["public"])
