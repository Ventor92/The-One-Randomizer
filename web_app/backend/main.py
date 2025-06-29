from fastapi import FastAPI
from routes import dice
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS - pozwala na łączenie się Reacta z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Na produkcji ustaw konkretną domenę Reacta
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dodanie endpointów
app.include_router(dice.router)