from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web_app.backend.routes.Users_Routers import router as user_router
from web_app.backend.routes.Chat_Routers import router as chat_router


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



@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}