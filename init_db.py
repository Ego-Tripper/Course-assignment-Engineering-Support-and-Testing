from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

# Import models and base class
from models import Base, Photo, Video, Book, UserDocument, Character, Review
from models import character_photo, character_video, character_book

# Настройка подключения к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./media_gallery.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Creating a Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables_and_indexes():
    """Создает все таблицы и индексы в базе данных"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
   # Creating Indexes Using Raw SQL
    with engine.connect() as conn:
        # Index to speed up the search for reviews by media object
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_review_media_composite 
            ON reviews (media_type, media_id);
        """))
        
        # Indexes for searching by name
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_photo_title 
            ON photos (title);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_video_title 
            ON videos (title);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_book_title 
            ON books (title);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_document_title 
            ON user_documents (title);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_character_name 
            ON characters (name);
        """))
        
        conn.commit()
    print("Таблицы и индексы успешно созданы")

def fill_test_data():
    """Заполняет базу тестовыми данными"""
    db = SessionLocal()
    
    try:
        # Create lists to store created objects
        photos = []
        videos = []
        books = []
        documents = []
        characters = []
        
        # Create 20 photos
        for i in range(1, 21):
            photo = Photo(
                title=f"Test Photo {i}",
                description=f"Description for photo {i}",
                file_path=f"/uploads/photo_{i}.jpg",
                file_size=1024 * i,
                file_type="image/jpeg",
                width=800,
                height=600,
                created_at=datetime.now()
            )
            photos.append(photo)
            db.add(photo)
        
        # Create 20 VIDEOS
        for i in range(1, 21):
            video = Video(
                title=f"Test Video {i}",
                description=f"Description for video {i}",
                file_path=f"/uploads/video_{i}.mp4",
                file_size=1024 * 1024 * i,  # MB
                file_type="video/mp4",
                width=1920,
                height=1080,
                duration=60 * i / 10,  # 6 seconds to 2 minutes
                created_at=datetime.now()
            )
            videos.append(video)
            db.add(video)
        
        # Create 20 Books
        for i in range(1, 21):
            book = Book(
                title=f"Test Book {i}",
                author=f"Author {i}",
                description=f"Description for book {i}",
                file_path=f"/uploads/book_{i}.pdf",
                file_size=1024 * 500 * i,  # КБ
                file_format="PDF",
                page_count=100 + i * 10,
                created_at=datetime.now()
            )
            books.append(book)
            db.add(book)
        
        # Create 20 Documents
        for i in range(1, 21):
            document = UserDocument(
                title=f"Test Document {i}",
                description=f"Description for document {i}",
                file_path=f"/uploads/document_{i}.docx",
                file_size=1024 * 50 * i,  # КБ
                review=f"Review for document {i}",
                created_at=datetime.now()
            )
            documents.append(document)
            db.add(document)
        
        # Create characters
        character_names = [
            "Harry Potter", "Hermione Granger", "Ron Weasley", 
            "Albus Dumbledore", "Severus Snape", "Lord Voldemort"
        ]
        
        for name in character_names:
            character = Character(
                name=name,
                description=f"Description of {name}"
            )
            characters.append(character)
            db.add(character)
        
        # Save all objects in the database
        db.commit()
        
        # Making many-to-many connections
        #The first character is connected to the first 5 photos, videos and books
        characters[0].photos.extend(photos[:5])
        characters[0].videos.extend(videos[:5])
        characters[0].books.extend(books[:5])
        
        # The second character is related to the following 5 photos, videos and books
        characters[1].photos.extend(photos[5:10])
        characters[1].videos.extend(videos[5:10])
        characters[1].books.extend(books[5:10])
        
        
        
        # Creating reviews
        media_types = ["photo", "video", "book", "document"]
        
        for i in range(20):  # Creating 20 reviews
            media_type = random.choice(media_types)
            
            if media_type == "photo":
                media_id = random.randint(1, 20)
            elif media_type == "video":
                media_id = random.randint(1, 20)
            elif media_type == "book":
                media_id = random.randint(1, 20)
            else:  # document
                media_id = random.randint(1, 20)
            
            review = Review(
                media_type=media_type,
                media_id=media_id,
                rating=random.randint(1, 10),
                comment=f"Comment for {media_type} {media_id}",
                created_at=datetime.now()
            )
            db.add(review)
        
        # Save all changes
        db.commit()
        print("Тестовые данные успешно добавлены")
        
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Creating tables and indexes
    create_tables_and_indexes()
    
    # Filling the database with test data
    fill_test_data()
    
    print("Инициализация базы данных завершена")