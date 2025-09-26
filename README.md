# Media Gallery on FastAPI

A web application for managing media content with the ability to add characters and reviews, implementing CRUD (Create, Read, Update, Delete) principles.

## 📋 About the Project

This project was developed as part of the course "Engineering Support for Information Systems. Part 1". The application allows managing various types of media files: photos, videos, books, and documents, with the ability to add reviews and link content to characters.

### Key Features

- **Media Content Management**: CRUD operations for photos, videos, books, and documents
- **Review System**: Adding ratings and comments to media files
- **Character Management**: Linking media files with characters (many-to-many)
- **REST API**: Fully functional API with Swagger documentation
- **Web Interface**: Basic web page for viewing and managing data
- **Search and Filtering**: Search across all media types and filter by various parameters

## 🛠 Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI** - modern web framework
- **SQLAlchemy** - ORM for database interaction
- **Pydantic** - data validation and serialization

### Database
- **SQLite** - relational database

### Frontend
- **Jinja2** - templating engine for web pages
- **Bootstrap** - styling framework

### Infrastructure
- **Docker** - application containerization
- **Docker Compose** - container orchestration
- **Nginx** - web server and reverse proxy

## 📁 Project Structure

media_gallery_fastapi/
├── app/                    # Main application
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # CRUD operations
│   ├── database.py        # Database setup
│   └── init_db.py         # Database initialization
├── templates/             # Jinja2 HTML templates
├── uploads/               # Folder for uploaded files
├── static/                # Static files (CSS, JS)
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── nginx.conf             # Nginx configuration
├── requirements.txt       # Python dependencies
└── README.md              # Documentation


## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+ (for local development)

### Running with Docker (recommended)

Clone the repository:

git clone https://github.com/Ego-Tripper/Course-assignment-Engineering-Support-and-Testing.git
cd Course-assignment-Engineering-Support-and-Testing

Start the application:

docker-compose up --build

Open your browser and go to:
Main application: http://localhost
API documentation: http://localhost/docs
Alternative documentation: http://localhost/redoc

Local Installation (without Docker)
Install dependencies:

pip install -r requirements.txt

Initialize the database:

python init_db.py

Start the server:

uvicorn main:app --reload

The application will be available at: http://localhost:8000

API Documentation
Main Endpoints
Media Files
GET /api/v1/photos/ - List of photos
POST /api/v1/photos/ - Create a photo
GET /api/v1/photos/{id} - Get a photo by ID
PUT /api/v1/photos/{id} - Update a photo
DELETE /api/v1/photos/{id} - Delete a photo
Characters
GET /api/v1/characters/ - List of characters
POST /api/v1/characters/ - Create a character
POST /api/v1/characters/{id}/photos/{photo_id} - Add a photo to a character
Reviews
GET /api/v1/reviews/ - List of reviews
POST /api/v1/reviews/ - Create a review (with rating check 1-10)
Search and Utilities
GET /api/v1/search?q=query - Search across all media
GET /api/v1/stats/ - Statistics on data
POST /api/v1/upload/ - Upload files

Example Requests:
# Get all photos
curl -X 'GET' 'http://localhost/api/v1/photos/'

# Create a new review
curl -X 'POST' 'http://localhost/api/v1/reviews/' \
  -H 'Content-Type: application/json' \
  -d '{
    "media_type": "photo",
    "media_id": 1,
    "rating": 9,
    "comment": "Great photo!"
  }'


🗃 Data Models

Main Entities

Photo - Photos
id, title, description, file_path, file_size, file_type, width, height, created_at
Video - Videos
id, title, description, file_path, file_size, file_type, width, height, duration, created_at
Book - Books
id, title, author, description, file_path, file_size, file_format, page_count, created_at
UserDocument - Documents
id, title, description, file_path, file_size, review, created_at
Auxiliary Entities

Character - Characters
id, name, description (many-to-many relationships with media)
Review - Reviews
id, media_type, media_id, rating (1-10), comment, created_at
🔧 Development

Adding New Features

Create a model in models.py
Add schemas in schemas.py
Implement CRUD operations in crud.py
Add endpoints in main.py
Testing:
# Run tests (if added)
pytest

# Check code style
flake8
black --check .
Linting and Formatting:
# Format code
black .

# Check style
flake8

🐛 Troubleshooting

Common Issues

Port 80 is occupied
Solution: Use port 8080 or stop the service occupying the port
Database error
Solution: Delete the media_gallery.db file and restart the application
Docker issues
Solution: Run docker system prune and rebuild the images
Logs and Debugging:
# View application logs
docker-compose logs app

# View Nginx logs
docker-compose logs nginx

# Check container status
docker-compose ps

🤝 Contributing

Fork the repository
Create a branch for the new feature (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push the branch (git push origin feature/amazing-feature)
Create a Pull Request
📄 License

This project is created for educational purposes and is distributed without a license.

👤 Authors

Ego-Tripper
GitHub: @Ego-Tripper
Pohenui
GitHub: @Pohenui

🙏 Acknowledgments

To the instructor, Vadim Anatolyevich Pomytkin
To the FastAPI community for excellent documentation
To the developers of SQLAlchemy and Pydantic
Note: This is an educational project created to demonstrate development skills in Python and FastAPI.