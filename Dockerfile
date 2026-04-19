FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for FastAPI (8000)
EXPOSE 8000

CMD ["uvicorn", "src.lims_vet.main:app", "--host", "0.0.0.0", "--port", "8000"]