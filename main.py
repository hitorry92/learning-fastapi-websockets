from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers.websocket_routes import router as websocket_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_root():
    return FileResponse('index.html')

app.include_router(websocket_router)
