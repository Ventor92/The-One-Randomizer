from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "mysql+pymysql://root:root1234@localhost:3306/ttrpg_new_origin"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# opcjonalnie, żeby utworzyć tabele w bazie:
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_engine():
    return engine
 