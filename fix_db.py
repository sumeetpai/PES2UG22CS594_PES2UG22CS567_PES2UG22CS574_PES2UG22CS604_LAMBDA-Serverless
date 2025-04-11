from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.models.function import Function
from app.core.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/serverless")

def fix_database():
    # Create engine and session
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Get all functions with NULL created_at
        functions = db.query(Function).filter(Function.created_at == None).all()
        
        # Update each function with current timestamp
        for function in functions:
            function.created_at = datetime.utcnow()
        
        # Commit changes
        db.commit()
        print(f"Updated {len(functions)} functions with created_at timestamps")
        
    except Exception as e:
        print(f"Error fixing database: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_database() 