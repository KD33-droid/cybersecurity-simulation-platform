FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY app.py .

# Expose detector port
EXPOSE 9000

# Run detector with unbuffered logs
CMD ["python", "-u", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]
