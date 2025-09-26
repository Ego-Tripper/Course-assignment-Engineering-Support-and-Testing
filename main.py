from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import crud
import models
import schemas
from database import SessionLocal, engine, get_db
from datetime import datetime
import shutil


# Create tables (if they haven't been created yet)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Media Gallery API",
    description="API для управления медиабиблиотекой с фотографиями, видео, книгами и документами",
    version="1.0.0"
)


# Create a download folder if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Basic endpoints
@app.get("/")
async def root():
    return {"message": "Media Gallery API is running", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Photo endpoints
@app.post("/api/v1/photos/", response_model=schemas.PhotoResponse)
def create_photo(photo: schemas.PhotoCreate, db: Session = Depends(get_db)):
    return crud.photo.create(db=db, obj_in=photo)

@app.get("/api/v1/photos/", response_model=List[schemas.PhotoResponse])
def read_photos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    photos = crud.photo.get_multi(db, skip=skip, limit=limit)
    return photos

@app.get("/api/v1/photos/{photo_id}", response_model=schemas.PhotoResponse)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = crud.photo.get(db, id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo

@app.put("/api/v1/photos/{photo_id}", response_model=schemas.PhotoResponse)
def update_photo(photo_id: int, photo: schemas.PhotoUpdate, db: Session = Depends(get_db)):
    db_photo = crud.photo.get(db, id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return crud.photo.update(db, db_obj=db_photo, obj_in=photo)

@app.delete("/api/v1/photos/{photo_id}")
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    db_photo = crud.photo.get(db, id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    crud.photo.delete(db, id=photo_id)
    return {"message": "Photo deleted successfully"}

# Video endpoints
@app.post("/api/v1/videos/", response_model=schemas.VideoResponse)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.video.create(db=db, obj_in=video)

@app.get("/api/v1/videos/", response_model=List[schemas.VideoResponse])
def read_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    videos = crud.video.get_multi(db, skip=skip, limit=limit)
    return videos

@app.get("/api/v1/videos/{video_id}", response_model=schemas.VideoResponse)
def read_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.video.get(db, id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video

@app.put("/api/v1/videos/{video_id}", response_model=schemas.VideoResponse)
def update_video(video_id: int, video: schemas.VideoUpdate, db: Session = Depends(get_db)):
    db_video = crud.video.get(db, id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return crud.video.update(db, db_obj=db_video, obj_in=video)

@app.delete("/api/v1/videos/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.video.get(db, id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    crud.video.delete(db, id=video_id)
    return {"message": "Video deleted successfully"}

# Book endpoints
@app.post("/api/v1/books/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.book.create(db=db, obj_in=book)

@app.get("/api/v1/books/", response_model=List[schemas.BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.book.get_multi(db, skip=skip, limit=limit)
    return books

@app.get("/api/v1/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.book.get(db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/api/v1/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.book.get(db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.book.update(db, db_obj=db_book, obj_in=book)

@app.delete("/api/v1/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.book.get(db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.book.delete(db, id=book_id)
    return {"message": "Book deleted successfully"}

# UserDocument endpoints
@app.post("/api/v1/documents/", response_model=schemas.UserDocumentResponse)
def create_document(document: schemas.UserDocumentCreate, db: Session = Depends(get_db)):
    return crud.user_document.create(db=db, obj_in=document)

@app.get("/api/v1/documents/", response_model=List[schemas.UserDocumentResponse])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = crud.user_document.get_multi(db, skip=skip, limit=limit)
    return documents

@app.get("/api/v1/documents/{document_id}", response_model=schemas.UserDocumentResponse)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.user_document.get(db, id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@app.put("/api/v1/documents/{document_id}", response_model=schemas.UserDocumentResponse)
def update_document(document_id: int, document: schemas.UserDocumentUpdate, db: Session = Depends(get_db)):
    db_document = crud.user_document.get(db, id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return crud.user_document.update(db, db_obj=db_document, obj_in=document)

@app.delete("/api/v1/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.user_document.get(db, id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    crud.user_document.delete(db, id=document_id)
    return {"message": "Document deleted successfully"}

# Character endpoints
@app.post("/api/v1/characters/", response_model=schemas.CharacterResponse)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    return crud.character.create(db=db, obj_in=character)

@app.get("/api/v1/characters/", response_model=List[schemas.CharacterResponse])
def read_characters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    characters = crud.character.get_multi(db, skip=skip, limit=limit)
    return characters

@app.get("/api/v1/characters/{character_id}", response_model=schemas.CharacterResponse)
def read_character(character_id: int, db: Session = Depends(get_db)):
    db_character = crud.character.get(db, id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character

@app.put("/api/v1/characters/{character_id}", response_model=schemas.CharacterResponse)
def update_character(character_id: int, character: schemas.CharacterUpdate, db: Session = Depends(get_db)):
    db_character = crud.character.get(db, id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return crud.character.update(db, db_obj=db_character, obj_in=character)

@app.delete("/api/v1/characters/{character_id}")
def delete_character(character_id: int, db: Session = Depends(get_db)):
    db_character = crud.character.get(db, id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    crud.character.delete(db, id=character_id)
    return {"message": "Character deleted successfully"}

# Character media management endpoints
@app.post("/api/v1/characters/{character_id}/photos/{photo_id}")
def add_photo_to_character(character_id: int, photo_id: int, db: Session = Depends(get_db)):
    result = crud.character.add_photo(db, character_id=character_id, photo_id=photo_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Character or Photo not found")
    return {"message": "Photo added to character successfully"}

@app.post("/api/v1/characters/{character_id}/videos/{video_id}")
def add_video_to_character(character_id: int, video_id: int, db: Session = Depends(get_db)):
    result = crud.character.add_video(db, character_id=character_id, video_id=video_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Character or Video not found")
    return {"message": "Video added to character successfully"}

@app.post("/api/v1/characters/{character_id}/books/{book_id}")
def add_book_to_character(character_id: int, book_id: int, db: Session = Depends(get_db)):
    result = crud.character.add_book(db, character_id=character_id, book_id=book_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Character or Book not found")
    return {"message": "Book added to character successfully"}

# Review endpoints
@app.post("/api/v1/reviews/", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    # Check the rating (must be from 1 to 10)
    if review.rating < 1 or review.rating > 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    return crud.review.create(db=db, obj_in=review)

@app.get("/api/v1/reviews/", response_model=List[schemas.ReviewResponse])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.review.get_multi(db, skip=skip, limit=limit)
    return reviews

@app.get("/api/v1/reviews/{review_id}", response_model=schemas.ReviewResponse)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.review.get(db, id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.put("/api/v1/reviews/{review_id}", response_model=schemas.ReviewResponse)
def update_review(review_id: int, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud.review.get(db, id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check the rating if it is provided
    if review.rating is not None and (review.rating < 1 or review.rating > 10):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    
    return crud.review.update(db, db_obj=db_review, obj_in=review)

@app.delete("/api/v1/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.review.get(db, id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    crud.review.delete(db, id=review_id)
    return {"message": "Review deleted successfully"}

# File upload endpoint
@app.post("/api/v1/upload/")
async def upload_file(
    file: UploadFile = File(...),
    media_type: str = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Generate a unique file name
    file_extension = os.path.splitext(file.filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{media_type}_{timestamp}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Get the file size
    file_size = os.path.getsize(file_path)
    
    # Create a database entry based on the media type
    if media_type == "photo":
        photo_data = schemas.PhotoCreate(
            title=title,
            description=description,
            file_path=file_path,
            file_size=file_size,
            file_type=file.content_type,
            width=0,  # You can add image processing to get the dimensions
            height=0
        )
        return crud.photo.create(db=db, obj_in=photo_data)
    
    elif media_type == "video":
        video_data = schemas.VideoCreate(
            title=title,
            description=description,
            file_path=file_path,
            file_size=file_size,
            file_type=file.content_type,
            width=0,
            height=0,
            duration=0  # You can add video processing to get the duration
        )
        return crud.video.create(db=db, obj_in=video_data)
    
    elif media_type == "book":
        book_data = schemas.BookCreate(
            title=title,
            author="Unknown",  # You can add an author field to the form
            description=description,
            file_path=file_path,
            file_size=file_size,
            file_format=file_extension[1:].upper(),  # PDF, EPUB, etc.
            page_count=None
        )
        return crud.book.create(db=db, obj_in=book_data)
    
    elif media_type == "document":
        document_data = schemas.UserDocumentCreate(
            title=title,
            description=description,
            file_path=file_path,
            file_size=file_size,
            review=description  # You can use the description as a review
        )
        return crud.user_document.create(db=db, obj_in=document_data)
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported media type")

# File download endpoint
@app.get("/api/v1/files/{file_path:path}")
async def download_file(file_path: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

# Search endpoint
@app.get("/api/v1/search/")
def search_media(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, description="Number of results per type"),
    db: Session = Depends(get_db)
):
    return crud.search_media(db, query=q, limit=limit)

# Additional search endpoints
@app.get("/api/v1/photos/search/")
def search_photos(
    q: str = Query(..., description="Search query for photos"),
    limit: int = Query(20, description="Number of results"),
    db: Session = Depends(get_db)
):
    return crud.photo.search_by_title(db, title=q, limit=limit)

@app.get("/api/v1/books/search/")
def search_books(
    q: str = Query(None, description="Search query for books by title"),
    author: str = Query(None, description="Search query for books by author"),
    limit: int = Query(20, description="Number of results"),
    db: Session = Depends(get_db)
):
    if author:
        return crud.book.search_by_author(db, author=author, limit=limit)
    elif q:
        return crud.book.search_by_title(db, title=q, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Provide either 'q' or 'author' parameter")

# Statistics endpoint
@app.get("/api/v1/stats/")
def get_statistics(db: Session = Depends(get_db)):
    from sqlalchemy import func
    
    photo_count = db.query(func.count(models.Photo.id)).scalar()
    video_count = db.query(func.count(models.Video.id)).scalar()
    book_count = db.query(func.count(models.Book.id)).scalar()
    document_count = db.query(func.count(models.UserDocument.id)).scalar()
    character_count = db.query(func.count(models.Character.id)).scalar()
    review_count = db.query(func.count(models.Review.id)).scalar()
    
    return {
        "photos": photo_count,
        "videos": video_count,
        "books": book_count,
        "documents": document_count,
        "characters": character_count,
        "reviews": review_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)