import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database.base import init_models
from database.models import *
from routes.product import router as product_router
from routes.user import router as user_router
from routes.home import router as home_router


app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(home_router)


app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/images", StaticFiles(directory="images"), name="images")


# origins = ['*']
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

    
if  __name__ == "__main__":
    #* Генерация таблиц выполняется запуском файла main.py, а не сервера
    # asyncio.run(init_models())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 