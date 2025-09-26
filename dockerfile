FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY models.py .
COPY database.py .
COPY init_db.py .
COPY crud.py .
COPY schemas.py .

RUN mkdir -p uploads
RUN chmod 755 uploads

EXPOSE 8000

CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]