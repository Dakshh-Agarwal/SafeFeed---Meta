FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency files first for build cache
COPY requirements.txt /app/requirements.txt

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only runtime files
COPY backend /app/backend
COPY server /app/server
COPY tasks /app/tasks
COPY inference.py /app/inference.py
COPY openenv.yaml /app/openenv.yaml
COPY README.md /app/README.md

EXPOSE 7860

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]
