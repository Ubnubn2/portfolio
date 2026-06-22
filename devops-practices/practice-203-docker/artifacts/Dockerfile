# Build stage
FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

# Runtime stage
FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["python", "app.py"]