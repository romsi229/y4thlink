from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routes.chat import router

app = FastAPI(title="Y4thLink API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)

@app.get("/")
def home():
    return FileResponse("app/static/index.html")
