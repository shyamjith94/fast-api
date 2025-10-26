from typing import Generator
from app.core import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text

class Database:
    def __init__(self,check_connection: bool=False):
        self._create_engine = create_engine(
            str(settings.SQLALCHEMY_DATABASE_URI),
            echo=settings.DATABASE_ECHO,
            future=True,
            
        )
        
        self._local_session =  sessionmaker(
           autoflush=False,
           autocommit=False,
           bind=self._create_engine,
           class_=Session,
           future=True
       )
        
        if check_connection:
            self._test_connection_once()

    def _test_connection_once(self):
        """Run once at initialization to confirm DB connectivity."""
        try:
            current_db = ""
            with self._create_engine.connect() as conn:
                current_db = conn.execute(text("SELECT current_database();")).scalar()
            print(f"Database connection successful! {current_db}")
        except Exception as e:
            print("Database connection failed:", e)
            raise e

    def get_db(self,)->Generator[Session,None, None]:
        db = self._local_session()
        try:
            yield db
        except Exception as e:
            print(str(e))
            db.rollback()
            raise
        finally:
            try:
                db.close()
            except Exception as e:
                print(str(e))
                
        
    
