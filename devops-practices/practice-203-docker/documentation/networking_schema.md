# Схема взаимодействия контейнеров

```mermaid
graph TD

User --> App

App --> PostgreSQL
App --> Redis

subgraph DockerNetwork
    App
    PostgreSQL
    Redis
end
```

## Описание

Все контейнеры работают во внутренней сети Docker.

Приложение взаимодействует с PostgreSQL для хранения данных и с Redis для кэширования запросов.

Данные PostgreSQL сохраняются через Docker Volume.
