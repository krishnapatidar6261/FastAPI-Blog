# main.py
import uvicorn
from fastapi import FastAPI
# from app.core import models as core_models
# from app.blogs import models as blogs_models
from database.session import engine
from app.blogs.api import router as blogs_router
from app.core.api import router as core_router


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Blog")
    # core_models.Base.metadata.create_all(bind=engine)
    # blogs_models.Base.metadata.create_all(bind=engine)

    app.include_router(core_router, tags=["Core"])
    app.include_router(blogs_router, prefix="/blogs", tags=["Blogs"])
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
