\# Описание security-этапов пайплайна



```mermaid

graph TD

&#x20;   A\[Push] --> B\[Gitleaks \& Trivy FS]

&#x20;   B --> C{Clean?}

&#x20;   C -->|Yes| D\[Docker Build \& Trivy Image]

&#x20;   C -->|No| E\[❌ Block]

#### 5. Обновление главного файла README.md
```