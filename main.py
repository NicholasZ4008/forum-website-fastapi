from fastapi import FastAPI, HTTPException, Depends, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import io
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class EmailModel(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_name = Column(String, unique=True, index=True, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class EmailBase(BaseModel):
    email_name: EmailStr

class EmailCreate(EmailBase):
    pass

class EmailUpdate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    
    class Config:
        from_attributes = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI(
    title="Forum Email API",
    description="A lightweight, efficient FastAPI for managing email subscriptions for The Forum University.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://theforumuniversity.com",
    "https://theforumuniversity.com",
    "http://www.theforumuniversity.com",
    "https://www.theforumuniversity.com",
    "http://api.theforumuniversity.com",
    "https://api.theforumuniversity.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Test database connection
@app.get("/test-connect")
async def test_connection(db: Session = Depends(get_db)):
    try:
        # Simple query to test connection
        db.execute("SELECT 1")
        return {"message": "Connected successfully to PostgreSQL!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot connect to PostgreSQL"
        )

# CRUD Endpoints

@app.get("/emails", response_model=List[Email])
async def get_emails(db: Session = Depends(get_db)):
    """Get all email subscriptions"""
    emails = db.query(EmailModel).all()
    return emails

@app.get("/emails/{email_id}", response_model=Email)
async def get_email(email_id: int, db: Session = Depends(get_db)):
    """Get a specific email subscription by ID"""
    email = db.query(EmailModel).filter(EmailModel.id == email_id).first()
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@app.post("/emails", response_model=Email, status_code=status.HTTP_201_CREATED)
async def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    """Add a new email subscription"""
    # Check if email already exists
    existing_email = db.query(EmailModel).filter(EmailModel.email_name == email.email_name).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    db_email = EmailModel(email_name=email.email_name)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

@app.put("/emails/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_email(email_id: int, email: EmailUpdate, db: Session = Depends(get_db)):
    """Update an existing email subscription"""
    db_email = db.query(EmailModel).filter(EmailModel.id == email_id).first()
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    # Check if the new email already exists (and it's not the same record)
    existing_email = db.query(EmailModel).filter(
        EmailModel.email_name == email.email_name,
        EmailModel.id != email_id
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    db_email.email_name = email.email_name
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.delete("/emails/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_email(email_id: int, db: Session = Depends(get_db)):
    """Remove an email subscription"""
    db_email = db.query(EmailModel).filter(EmailModel.id == email_id).first()
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    db.delete(db_email)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/export")
async def export_emails(db: Session = Depends(get_db)):
    """Export all emails as CSV"""
    emails = db.query(EmailModel).all()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(["Id", "EmailName"])
    
    # Write data rows
    for email in emails:
        writer.writerow([email.id, email.email_name])
    
    # Get CSV content
    csv_content = output.getvalue()
    output.close()
    
    # Return as streaming response
    return StreamingResponse(
        io.BytesIO(csv_content.encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=emails.csv"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)