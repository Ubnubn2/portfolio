# Практика 203 — Контейнеризация и воспроизводимость окружения

## Проект

LinkShort — сервис сокращения URL.

## Docker Image

https://hub.docker.com/r/Ubnubn2/linkshort

## Запуск проекта

```bash
docker-compose up -d
```

## Сервисы

* app — FastAPI приложение
* db — PostgreSQL 16
* cache — Redis 7

## Остановка

```bash
docker-compose down
```

## Используемые технологии

* Python 3.12
* FastAPI
* PostgreSQL
* Redis
* Docker
* Docker Compose
* GitHub Actions
