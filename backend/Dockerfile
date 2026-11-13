# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY shared ./shared

# Expose port
EXPOSE 8000

# Set environment variable for SQLite path (relative to /app/shared)
ENV DATABASE_URL=sqlite:////app/shared/database.db

# Command to run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
