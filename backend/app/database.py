from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///focusboard.db", echo=True)  

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False                        
)

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()