#!/usr/bin/env python
# coding: utf-8

# In[1]:


# ============================================================
# AI-POWERED SECURE DOCUMENT SEARCH PORTAL
# PYTHON TEAM - BATCH 1
# ============================================================

# 1. INSTALL REQUIRED LIBRARIES


# ============================================================
# 2. IMPORT LIBRARIES
# ============================================================

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from pathlib import Path
import requests
import threading
import uvicorn


# ============================================================
# 3. CREATE UPLOAD FOLDER
# ============================================================

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


# ============================================================
# 4. DATABASE SETTINGS
# ============================================================

DATABASE_URL = "sqlite:///./documents.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


# ============================================================
# 5. DATABASE TABLE
# ============================================================

class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )


Base.metadata.create_all(bind=engine)


# ============================================================
# 6. CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="Python Team Document Backend",
    description="Backend for the AI-Powered Secure Document Search Portal",
    version="1.0"
)


# ============================================================
# 7. ALLOW WEB FRONTEND TO CONNECT
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# 8. PYDANTIC MODEL FOR AI QUESTION
# ============================================================

class AskQuestion(BaseModel):
    document_id: int
    question: str


# ============================================================
# 9. HOME API
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Python Backend is running",
        "docs": "http://127.0.0.1:8000/docs"
    }


# ============================================================
# 10. UPLOAD DOCUMENT
# ============================================================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a file."
        )

    # TXT files only
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only TXT files are allowed."
        )

    # Read file
    file_data = await file.read()

    # Convert bytes to text
    try:
        text = file_data.decode("utf-8")

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="The file must be a UTF-8 TXT file."
        )

    # Check empty file
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="File is empty."
        )

    # Keep only file name
    safe_name = Path(file.filename).name

    # Save file in uploads folder
    file_path = UPLOAD_FOLDER / safe_name
    file_path.write_text(
        text,
        encoding="utf-8"
    )

    # Save document in SQLite
    db: Session = SessionLocal()

    try:

        document = Document(
            filename=safe_name,
            content=text
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "message": "Document uploaded successfully",
            "document_id": document.id,
            "filename": document.filename
        }

    finally:
        db.close()


# ============================================================
# 11. SHOW ALL DOCUMENTS
# ============================================================

@app.get("/documents")
def get_documents():

    db: Session = SessionLocal()

    try:

        documents = db.query(Document).all()

        result = []

        for document in documents:

            result.append({
                "id": document.id,
                "filename": document.filename
            })

        return result

    finally:
        db.close()


# ============================================================
# 12. READ ONE DOCUMENT
# ============================================================

@app.get("/documents/{document_id}")
def get_document(document_id: int):

    db: Session = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        return {
            "id": document.id,
            "filename": document.filename,
            "content": document.content
        }

    finally:
        db.close()


# ============================================================
# 13. SIMPLE KEYWORD SEARCH
# ============================================================

@app.get("/search")
def search_documents(keyword: str):

    keyword = keyword.strip()

    if not keyword:

        raise HTTPException(
            status_code=400,
            detail="Please enter a keyword."
        )

    db: Session = SessionLocal()

    try:

        documents = db.query(Document).all()

        results = []

        for document in documents:

            if keyword.lower() in document.content.lower():

                results.append({
                    "id": document.id,
                    "filename": document.filename
                })

        return {
            "keyword": keyword,
            "total_results": len(results),
            "results": results
        }

    finally:
        db.close()


# ============================================================
# 14. DOWNLOAD DOCUMENT
# ============================================================

@app.get("/download/{document_id}")
def download_document(document_id: int):

    db: Session = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        headers = {
            "Content-Disposition":
            f'attachment; filename="{document.filename}"'
        }

        return Response(
            content=document.content,
            media_type="text/plain",
            headers=headers
        )

    finally:
        db.close()


# ============================================================
# 15. DELETE DOCUMENT
# ============================================================

@app.delete("/documents/{document_id}")
def delete_document(document_id: int):

    db: Session = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        db.delete(document)
        db.commit()

        return {
            "message": "Document deleted successfully"
        }

    finally:
        db.close()


# ============================================================
# 16. AI TEAM CONNECTION
# ============================================================

# AI Team will provide the real URL later.
AI_TEAM_URL = "http://127.0.0.1:8001/ask"


@app.post("/ask-ai")
def ask_ai(request: AskQuestion):

    # Step 1: Get document from database
    db: Session = SessionLocal()

    try:

        document = (
            db.query(Document)
            .filter(Document.id == request.document_id)
            .first()
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        # Step 2: Prepare data for AI Team
        data = {
            "document_id": document.id,
            "document_name": document.filename,
            "document_text": document.content,
            "question": request.question
        }

        # Step 3: Send data to AI Team
        try:

            response = requests.post(
                AI_TEAM_URL,
                json=data,
                timeout=30
            )

        except requests.exceptions.RequestException:

            raise HTTPException(
                status_code=503,
                detail="AI Team server is not connected yet."
            )

        # Step 4: Check AI response
        if response.status_code != 200:

            raise HTTPException(
                status_code=500,
                detail="AI Team returned an error."
            )

        # Step 5: Read AI answer
        ai_answer = response.json()

        # Step 6: Return answer to Web Team
        return {
            "document": document.filename,
            "question": request.question,
            "answer": ai_answer
        }

    finally:
        db.close()


# ============================================================
# 17. COUNT DOCUMENTS
# ============================================================

@app.get("/count")
def count_documents():

    db: Session = SessionLocal()

    try:

        total = db.query(Document).count()

        return {
            "total_documents": total
        }

    finally:
        db.close()


# ============================================================
# 18. START SERVER
# ============================================================

def start_server():

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )


server_thread = threading.Thread(
    target=start_server,
    daemon=True
)

server_thread.start()


# ============================================================
# 19. FINAL MESSAGE
# ============================================================

print("=" * 60)
print("PYTHON TEAM PROJECT STARTED")
print("=" * 60)

print("Backend: http://127.0.0.1:8000")
print("API Testing: http://127.0.0.1:8000/docs")
print("AI Team API: " + AI_TEAM_URL)

print("=" * 60)


# In[ ]:




