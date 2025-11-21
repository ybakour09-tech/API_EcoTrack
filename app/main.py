from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import routes_auth, routes_indicators, routes_sources, routes_stats, routes_users, routes_zones
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    app = FastAPI(title=settings.project_name, version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routes_auth.router, prefix=settings.api_v1_prefix)
    app.include_router(routes_users.router, prefix=settings.api_v1_prefix)
    app.include_router(routes_zones.router, prefix=settings.api_v1_prefix)
    app.include_router(routes_sources.router, prefix=settings.api_v1_prefix)
    app.include_router(routes_indicators.router, prefix=settings.api_v1_prefix)
    app.include_router(routes_stats.router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["health"])
    def healthcheck():
        return {"status": "ok"}

    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
