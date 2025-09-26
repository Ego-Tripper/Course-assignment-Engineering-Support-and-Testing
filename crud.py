from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional, Type, TypeVar, Generic
from models import Photo, Video, Book, UserDocument, Character, Review
import schemas

ModelType = TypeVar('ModelType')

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: schemas.BaseModel) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: schemas.BaseModel) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

# Photo CRUD
class CRUDPhoto(CRUDBase[Photo]):
    def search_by_title(self, db: Session, title: str, limit: int = 20) -> List[Photo]:
        return db.query(Photo).filter(Photo.title.ilike(f"%{title}%")).limit(limit).all()
    
    def get_by_character(self, db: Session, character_id: int) -> List[Photo]:
        character = db.query(Character).filter(Character.id == character_id).first()
        return character.photos if character else []

photo = CRUDPhoto(Photo)

# Video CRUD
class CRUDVideo(CRUDBase[Video]):
    def search_by_title(self, db: Session, title: str, limit: int = 20) -> List[Video]:
        return db.query(Video).filter(Video.title.ilike(f"%{title}%")).limit(limit).all()
    
    def get_by_character(self, db: Session, character_id: int) -> List[Video]:
        character = db.query(Character).filter(Character.id == character_id).first()
        return character.videos if character else []

video = CRUDVideo(Video)

# Book CRUD
class CRUDBook(CRUDBase[Book]):
    def search_by_title(self, db: Session, title: str, limit: int = 20) -> List[Book]:
        return db.query(Book).filter(Book.title.ilike(f"%{title}%")).limit(limit).all()
    
    def search_by_author(self, db: Session, author: str, limit: int = 20) -> List[Book]:
        return db.query(Book).filter(Book.author.ilike(f"%{author}%")).limit(limit).all()
    
    def get_by_character(self, db: Session, character_id: int) -> List[Book]:
        character = db.query(Character).filter(Character.id == character_id).first()
        return character.books if character else []

book = CRUDBook(Book)

# UserDocument CRUD
class CRUDUserDocument(CRUDBase[UserDocument]):
    def search_by_title(self, db: Session, title: str, limit: int = 20) -> List[UserDocument]:
        return db.query(UserDocument).filter(UserDocument.title.ilike(f"%{title}%")).limit(limit).all()

user_document = CRUDUserDocument(UserDocument)

# Character CRUD
class CRUDCharacter(CRUDBase[Character]):
    def search_by_name(self, db: Session, name: str, limit: int = 20) -> List[Character]:
        return db.query(Character).filter(Character.name.ilike(f"%{name}%")).limit(limit).all()
    
    def add_photo(self, db: Session, character_id: int, photo_id: int) -> Character:
        character = self.get(db, character_id)
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if character and photo:
            character.photos.append(photo)
            db.commit()
            db.refresh(character)
        return character
    
    def add_video(self, db: Session, character_id: int, video_id: int) -> Character:
        character = self.get(db, character_id)
        video = db.query(Video).filter(Video.id == video_id).first()
        if character and video:
            character.videos.append(video)
            db.commit()
            db.refresh(character)
        return character
    
    def add_book(self, db: Session, character_id: int, book_id: int) -> Character:
        character = self.get(db, character_id)
        book = db.query(Book).filter(Book.id == book_id).first()
        if character and book:
            character.books.append(book)
            db.commit()
            db.refresh(character)
        return character

character = CRUDCharacter(Character)

# Review CRUD
class CRUDReview(CRUDBase[Review]):
    def get_by_media(self, db: Session, media_type: schemas.MediaType, media_id: int) -> List[Review]:
        return db.query(Review).filter(
            Review.media_type == media_type.value,
            Review.media_id == media_id
        ).all()
    
    def get_average_rating(self, db: Session, media_type: schemas.MediaType, media_id: int) -> Optional[float]:
        from sqlalchemy import func
        result = db.query(func.avg(Review.rating)).filter(
            Review.media_type == media_type.value,
            Review.media_id == media_id
        ).scalar()
        return float(result) if result else None
    
    def get_by_rating_range(self, db: Session, min_rating: int, max_rating: int, limit: int = 20) -> List[Review]:
        return db.query(Review).filter(
            and_(Review.rating >= min_rating, Review.rating <= max_rating)
        ).limit(limit).all()

review = CRUDReview(Review)

# Global search function
def search_media(db: Session, query: str, limit: int = 20) -> dict:
    """Search across all media types"""
    photos = photo.search_by_title(db, query, limit)
    videos = video.search_by_title(db, query, limit)
    books = book.search_by_title(db, query, limit)
    documents = user_document.search_by_title(db, query, limit)
    characters = character.search_by_name(db, query, limit)
    
    return {
        "photos": photos,
        "videos": videos,
        "books": books,
        "documents": documents,
        "characters": characters
    }