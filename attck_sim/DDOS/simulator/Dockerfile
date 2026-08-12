FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn requests

# Copy application code
COPY app.py .

# Expose UI port
EXPOSE 3000

# Run simulator with unbuffered logs
CMD ["python", "-u", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
