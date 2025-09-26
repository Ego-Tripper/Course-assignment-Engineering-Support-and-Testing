from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base class for all models
Base = declarative_base()

# Associative tables for many-to-many relationships
character_photo = Table(
    'character_photo', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('photo_id', Integer, ForeignKey('photos.id'), primary_key=True)
)

character_video = Table(
    'character_video', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('video_id', Integer, ForeignKey('videos.id'), primary_key=True)
)

character_book = Table(
    'character_book', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True)
)

class Photo(Base):
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    file_path = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with Character (many-to-many) - use backref instead of back_populates
    characters = relationship("Character", secondary=character_photo, backref="photos")

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    file_path = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    characters = relationship("Character", secondary=character_video, backref="videos")

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
    
    characters = relationship("Character", secondary=character_book, backref="books")

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
    
    # Removed explicit relationships since we use backref
    # Links will be available via backref: character.photos, character.videos, etc.

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    media_type = Column(String)  # 'photo', 'video', 'book', 'document'
    media_id = Column(Integer)   # ID of the entity of the specified type
    rating = Column(Integer)     # Rating from 1 to 10
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime)