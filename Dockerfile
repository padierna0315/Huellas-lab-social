FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Copy application and install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Expose ports for FastAPI
EXPOSE 8080

CMD ["sh", "-c", "uvicorn lims_vet.main:app --host 0.0.0.0 --port $PORT"]