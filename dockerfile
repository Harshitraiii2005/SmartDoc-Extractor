FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt /app/
COPY app.py /app/
COPY templates /app/templates/
COPY static /app/static/
COPY fonts /app/fonts/
COPY frontend /app/frontend/
COPY trained_invoice_ner /app/trained_invoice_ner/


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]