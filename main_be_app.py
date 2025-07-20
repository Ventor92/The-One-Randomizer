from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web_app.backend.routes.rollHistory import router as roll_history_router
from web_app.backend.routes.websocket import router as websocket_router
from web_app.backend.routes.Users_Routers import router as database_router
from web_app.backend.routes.Chat_Routers import router as chat_router

from web_app.backend.database.Chat_DB import Chat_DB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roll_history_router)
app.include_router(websocket_router)
app.include_router(database_router)
app.include_router(chat_router)



@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}