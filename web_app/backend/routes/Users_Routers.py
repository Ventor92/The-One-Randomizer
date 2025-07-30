from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel
from typing import List, Optional, Literal
import time

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..database.database import create_db_and_tables, get_session
from ..models.User import User

router = APIRouter(
    prefix="/api/users",
    tags=["database"]
)


@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/all", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.get("/", response_model=User)
def read_user(user_id: int = Query(None, description="User Id"),
              session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user