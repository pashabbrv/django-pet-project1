# Сервис бронирования отелей

## Запуск

Для запуска необходим Docker с поддержкой Docker Compose.

1. Скопировать `.env.example` в `.env`.
2. Запустить приложение:

```bash
docker compose up -d --build
```

API будет доступен по адресу `http://localhost:9000`.

Для остановки:

```bash
docker compose down
```

## API

Все методы работают без авторизации. Ответы и ошибки возвращаются в JSON.

### 1. Создание номера

`POST /rooms/create`

Принимает описание номера и цену за ночь.

```bash
curl -X POST http://localhost:9000/rooms/create -d "description=Double room" -d "price_per_night=3500.00"
```

Ответ:

```json
{"room_id": 1}
```

### 2. Список номеров

`GET /rooms/list`

Возвращает список номеров. Поддерживается сортировка по цене (`price`) и дате создания (`created_at`), по возрастанию (`asc`) и убыванию (`desc`).

```bash
curl "http://localhost:9000/rooms/list?sort_by=price&order=asc"
```

Пример ответа:

```json
[
  {
    "id": 1,
    "description": "Double room",
    "price_per_night": "3500.00",
    "created_at": "2026-11-08T15:00:00Z"
  }
]
```

### 3. Удаление номера

`DELETE /rooms/delete`

Принимает ID номера. Вместе с номером удаляются все связанные бронирования.

```bash
curl -X DELETE "http://localhost:9000/rooms/delete?room_id=1"
```

### 4. Создание бронирования

`POST /bookings/create`

Принимает ID существующего номера, дату начала и дату окончания бронирования.

```bash
curl -X POST http://localhost:9000/bookings/create -d "room_id=1" -d "date_start=2027-01-10" -d "date_end=2027-01-15"
```

Ответ:

```json
{"booking_id": 1}
```

### 5. Список бронирований номера

`GET /bookings/list`

Принимает ID номера и возвращает его бронирования, отсортированные по дате начала.

```bash
curl "http://localhost:9000/bookings/list?room_id=1"
```

Пример ответа:

```json
[
  {
    "booking_id": 1,
    "date_start": "2027-01-10",
    "date_end": "2027-01-15"
  }
]
```

### 6. Удаление бронирования

`DELETE /bookings/delete`

Принимает ID бронирования.

```bash
curl -X DELETE "http://localhost:9000/bookings/delete?booking_id=1"
```

## Тесты

Для запуска тестов необходимо установить Python и Poetry, а также запустить PostgreSQL.

```bash
poetry install --with dev
poetry run pytest -q
```
