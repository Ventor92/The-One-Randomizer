from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from web_app.backend.database.database import create_db_and_tables, get_session

from web_app.backend.routes.Users_Routers import router as user_router
from web_app.backend.routes.Chat_Routers import router as chat_router
from web_app.backend.routes.Character_Routers import router as character_router
from web_app.backend.routes.Table_Router import router as table_router
from web_app.backend.routes.TableEnhanced_Router import router as tableEnhanced_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(chat_router)
app.include_router(character_router)
app.include_router(table_router)
app.include_router(tableEnhanced_router)


create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}