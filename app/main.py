from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes.chat import router

app = FastAPI(title="Y4thLink API")

app.include_router(router)

@app.get("/")
def home():
    return JSONResponse(
        content={"message": "Y4thLink est en ligne 🌿"},
        media_type="application/json; charset=utf-8"
    )
