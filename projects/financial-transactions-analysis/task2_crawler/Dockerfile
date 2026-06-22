FROM python:3.11-slim

# Устанавливаем системные зависимости (для работы с RAR)
RUN apt-get update && apt-get install -y \
    unrar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

CMD ["python", "scripts/generate_files.py"]