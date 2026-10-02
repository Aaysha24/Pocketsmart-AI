from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.staticfiles import (
    StaticFiles
)

from .config import (
    APP_NAME,
    BASE_DIR
)

from .database import (
    Base,
    engine
)

from .routes import router


# =========================================================
# APPLICATION LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    # Create database tables
    Base.metadata.create_all(
        bind=engine
    )

    yield


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(

    title=APP_NAME,

    version="1.0.0",

    lifespan=lifespan
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(

    "/static",

    StaticFiles(
        directory=str(
            BASE_DIR / "static"
        )
    ),

    name="static"
)


# =========================================================
# ROUTES
# =========================================================

app.include_router(
    router
)


# =========================================================
# HEALTH
# =========================================================

@app.get(
    "/health"
)
def health():

    return {

        "status": "ok",

        "service": APP_NAME
    }


# =========================================================
# STARTUP
# =========================================================

@app.get(
    "/startup"
)
def startup_status():

    return {

        "status": "ready",

        "service": APP_NAME
    }


# =========================================================
# DIRECT RUN
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )
    