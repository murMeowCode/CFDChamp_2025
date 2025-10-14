FROM python:3.11-slim

WORKDIR /profile_service

RUN mkdir -p /profile_service/shared

COPY shared/ /profile_service/shared/
COPY requirements.txt /profile_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY profile_service/ /profile_service/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
