from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base=declarative_base()

#Create Tables
character_photo = Table(
    'character_photo', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('photo_id', Integer, ForeignKey('photos.id'))
)

character_video = Table(
    'character_video', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('video_id', Integer, ForeignKey('videos.id'))
)

character_book = Table(
    'character_book', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)

#Create models
class Photo(Base):

    __tablename__="photos"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String, index=True)
    description=Column(Text, nullable=True)
    file_path = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship to Character (many-to-many)
    character =relationship("Character", secondary=character_photo, back_populates="photos")

class Video(Base):

    __tablename__="videos"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String, index=True)
    description=Column(Text, nullable=True)
    file_path = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship to Character (many-to-many)
    character =relationship("Character", secondary=character_video, back_populates="videos")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(Text, nullable=True)
    file_path = Column(String)
    file_size = Column(Integer)
    file_format = Column(String)
    page_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship to Character (many-to-many)
    character =relationship("Character", secondary=character_book, back_populates="books")

class UserDocument(Base):
    __tablename__ = "user_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    file_path = Column(String)
    file_size = Column(Integer)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    # Media Entity Relationships (Many-to-Many)
    photos = relationship("Photo", secondary=character_photo, back_populates="characters")
    videos = relationship("Video", secondary=character_video, back_populates="characters")
    books = relationship("Book", secondary=character_book, back_populates="characters")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    media_type = Column(String)  # 'photo', 'video', 'book', 'document'
    media_id = Column(Integer)   # Entity ID of the specified type
    rating = Column(Integer)     # Rating from 1 to 10
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Unique index per pair (media_type, media_id)
    __table_args__ = (
    # Unique constraint to prevent more than one review of a media object # Index('idx_review_media_composite', 'media_type', 'media_id', unique=True),)
    )

