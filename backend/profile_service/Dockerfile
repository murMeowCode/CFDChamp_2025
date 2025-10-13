FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/shared

COPY shared/ /app/shared/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY profile_service/ /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
