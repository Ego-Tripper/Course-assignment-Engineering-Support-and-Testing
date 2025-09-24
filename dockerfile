FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-chache-dir -r requirements.txt

COPY main.py .
COPY models.py .
COPY database.py .
COPY init_db.py .
COPY crud.py .
COPY schemas.py .

RUN mkidr -p uploads

RUN chmod 755 uploads

RUN python init_db.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]