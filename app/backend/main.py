from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.backend.config import settings
from app.backend.routers import riders, races

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(riders.rider_router, prefix = "/api")
app.include_router(races.race_router, prefix = "/api")


@app.on_event("startup")
async def startup_event():
    print(f"🏍️  {settings.app_name} v{settings.app_version} starting...")
    print(f"📡 Environment: {settings.environment}")
    print(f"🔧 Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Shutting down...")


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs"
    }
