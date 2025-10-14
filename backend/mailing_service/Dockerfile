FROM python:3.11-slim

WORKDIR /mailing_service

RUN mkdir -p /mailing_service/shared

COPY shared/ /mailing_service/shared/
COPY requirements.txt /mailing_service/

RUN pip install --no-cache-dir -r requirements.txt

COPY mailing_service/ /mailing_service/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
