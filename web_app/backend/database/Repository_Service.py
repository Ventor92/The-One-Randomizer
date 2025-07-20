from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

T = TypeVar("T")  # Typ modelu

class RepositoryService(Generic[T]):
    model: Type[T]

    @classmethod
    def get(cls, db: Session, id: int) -> Optional[T]:
        return db.get(cls.model, id)

    @classmethod
    def add(cls, db: Session, obj: T) -> T:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @classmethod
    def update(cls, db: Session, obj: T) -> T:
        db.commit()
        db.refresh(obj)
        return obj

    @classmethod
    def delete(cls, db: Session, obj: T) -> None:
        db.delete(obj)
        db.commit()

    @classmethod
    def get_all(cls, db: Session) -> List[T]:
        return db.query(cls.model).all()