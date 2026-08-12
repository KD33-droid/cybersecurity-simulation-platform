FROM python:3.11-slim

WORKDIR /workspace/Launcher

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io curl && \
    apt-get clean

# Install docker-compose manually
RUN curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Python deps
RUN pip install fastapi uvicorn requests

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
