# MillServer

Servrer for Mill game

## Для разработчиков

### Требования

1. [Python](https://python.org) 3.12 и выше
2. [Poetry](https://python-poetry.org) 3.8 и выше

### Локальный запуск

Команды нужно выполнять в корне проекта

#### Установка библиотек и создание виртуального окружения

```shell
poetry install
```

#### Локальный запуск

```shell
poetry run dev
```

### Запуск тестов

#### mypy - анализатор типов

```shell
mypy .
```

#### ruff - линтер & форматер

```shell
ruff check --fix
```