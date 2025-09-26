from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum

class MediaType(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    BOOK = "book"
    DOCUMENT = "document"

# Base schemas
class PhotoBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    file_size: int
    file_type: str
    width: Optional[int] = None
    height: Optional[int] = None

class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    file_size: int
    file_type: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    file_path: str
    file_size: int
    file_format: str
    page_count: Optional[int] = None

class UserDocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    file_size: int
    review: Optional[str] = None

class CharacterBase(BaseModel):
    name: str
    description: Optional[str] = None

class ReviewBase(BaseModel):
    media_type: MediaType
    media_id: int
    rating: int
    comment: Optional[str] = None

# Create schemas (for POST requests)
class PhotoCreate(PhotoBase):
    pass

class VideoCreate(VideoBase):
    pass

class BookCreate(BookBase):
    pass

class UserDocumentCreate(UserDocumentBase):
    pass

class CharacterCreate(CharacterBase):
    pass

class ReviewCreate(ReviewBase):
    pass

# Update schemas (for PUT/PATCH requests)
class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None

class UserDocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    review: Optional[str] = None

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

# Response schemas (for GET requests)
class PhotoResponse(PhotoBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class VideoResponse(VideoBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BookResponse(BookBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserDocumentResponse(UserDocumentBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CharacterResponse(CharacterBase):
    id: int
    photos: List[PhotoResponse] = []
    videos: List[VideoResponse] = []
    books: List[BookResponse] = []
    model_config = ConfigDict(from_attributes=True)

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Simplified response schemas for relationships
class PhotoSimpleResponse(BaseModel):
    id: int
    title: str
    file_path: str
    model_config = ConfigDict(from_attributes=True)

class VideoSimpleResponse(BaseModel):
    id: int
    title: str
    file_path: str
    model_config = ConfigDict(from_attributes=True)

class BookSimpleResponse(BaseModel):
    id: int
    title: str
    author: str
    file_path: str
    model_config = ConfigDict(from_attributes=True)

# Search and filter schemas
class SearchQuery(BaseModel):
    query: str
    limit: int = 20
    offset: int = 0

class MediaFilter(BaseModel):
    media_type: Optional[MediaType] = None
    min_rating: Optional[int] = None
    max_rating: Optional[int] = None
    limit: int = 20
    offset: int = 0