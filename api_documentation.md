# API Documentation

## Introduction
This documentation describes the API for a mobile application supporting users with PTSD. The API provides functionality for user registration and authentication, profile management, emergency assistance, and support chat.

## Base URL
All API endpoints have the prefix `/api/v1/`.

## Authentication
Most endpoints require authentication using a token. Include the token in the request header:
```
Authorization: Token <your_token>
```

The token can be obtained through the `/api/v1/user/login/` endpoint.

## Error Codes
The API uses standard HTTP status codes:
- `200 OK`: Request completed successfully
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request (check request data)
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied (no permissions)
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Internal server error

## User API

### User Registration
Creates a new user in the system.

- **URL**: `/api/v1/user/registration/`
- **Method**: POST
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "username",
    "email": "email@example.com",
    "password": "password"
  }
  ```
  | Field | Type | Required | Description |
  |------|-----|--------------|----------|
  | username | string | Yes | Unique username |
  | email | string | Yes | User's email address |
  | password | string | Yes | User's password |

- **Response**:
  - Success (201 Created):
    ```json
    {
      "message": "User Created"
    }
    ```
  - Error (400 Bad Request):
    ```json
    {
      "username": ["A user with that username already exists."],
      "email": ["Enter a valid email address."],
      "password": ["This field is required."]
    }
    ```

- **Request Example**:
  ```bash
  curl -X POST \
    http://127.0.0.1:8000/api/v1/user/registration/ \
    -H 'Content-Type: application/json' \
    -d '{
      "username": "testuser",
      "email": "test@example.com",
      "password": "securepassword123"
    }'
  ```

### Вход пользователя
Аутентифицирует пользователя и возвращает токен для дальнейших запросов.

- **URL**: `/api/v1/user/login/`
- **Метод**: POST
- **Аутентификация**: Не требуется
- **Тело запроса**:
  ```json
  {
    "username": "имя_пользователя",
    "password": "пароль"
  }
  ```
  | Поле | Тип | Обязательное | Описание |
  |------|-----|--------------|----------|
  | username | string | Да | Имя пользователя |
  | password | string | Да | Пароль пользователя |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "token": "a1b2c3d4e5f6g7h8i9j0"
    }
    ```
  - Ошибка (401 Unauthorized):
    ```json
    {
      "error": "Invalid credentials."
    }
    ```
  - Ошибка (400 Bad Request):
    ```json
    {
      "error": "Username and password are required."
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X POST \
    http://127.0.0.1:8000/api/v1/user/login/ \
    -H 'Content-Type: application/json' \
    -d '{
      "username": "testuser",
      "password": "securepassword123"
    }'
  ```

### Получение информации о пользователе
Возвращает подробную информацию о профиле пользователя.

- **URL**: `/api/v1/user/{user_id}/`
- **Метод**: GET
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "id": 1,
      "user": 1,
      "username": "testuser",
      "age": 30,
      "location": "Москва",
      "military_status": true,
      "ptsd_level": 3,
      "music": 2,
      "therapist_contact": 1,
      "scenario": 1
    }
    ```
    | Поле | Тип | Описание |
    |------|-----|----------|
    | id | integer | ID профиля пользователя |
    | user | integer | ID пользователя |
    | username | string | Имя пользователя |
    | age | integer | Возраст пользователя |
    | location | string | Местоположение пользователя |
    | military_status | boolean | Военный статус (true - военный, false - гражданский) |
    | ptsd_level | integer | Уровень ПТСР (от 1 до 5) |
    | music | integer | ID выбранного музыкального трека |
    | therapist_contact | integer | ID контакта терапевта |
    | scenario | integer | ID выбранного сценария тревоги |

  - Ошибка (404 Not Found):
    ```json
    {
      "error": "UserInfo not found for this user."
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X GET \
    http://127.0.0.1:8000/api/v1/user/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0'
  ```

### Редактирование информации о пользователе
Обновляет информацию в профиле пользователя.

- **URL**: `/api/v1/user/edit/{user_id}/`
- **Метод**: PATCH
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Тело запроса**:
  ```json
  {
    "age": 35,
    "location": "Санкт-Петербург",
    "military_status": true,
    "ptsd_level": 2,
    "therapist_contact": 2,
    "scenario": 3
  }
  ```
  | Поле | Тип | Обязательное | Описание |
  |------|-----|--------------|----------|
  | age | integer | Нет | Возраст пользователя |
  | location | string | Нет | Местоположение пользователя |
  | military_status | boolean | Нет | Военный статус |
  | ptsd_level | integer | Нет | Уровень ПТСР (от 1 до 5) |
  | therapist_contact | integer | Нет | ID контакта терапевта |
  | scenario | integer | Нет | ID сценария тревоги |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "message": "UserInfo updated successfully.",
      "updated_data": {
        "age": 35,
        "location": "Санкт-Петербург",
        "military_status": true,
        "ptsd_level": 2,
        "therapist_contact": 2,
        "scenario": 3
      }
    }
    ```
  - Ошибка (404 Not Found):
    ```json
    {
      "error": "UserInfo not found for this user."
    }
    ```
  - Ошибка (400 Bad Request):
    ```json
    {
      "error": "AlarmScenario not found with this id."
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X PATCH \
    http://127.0.0.1:8000/api/v1/user/edit/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0' \
    -H 'Content-Type: application/json' \
    -d '{
      "age": 35,
      "location": "Санкт-Петербург",
      "ptsd_level": 2
    }'
  ```

### Редактирование экстренного контакта
Создает или обновляет экстренный контакт для пользователя.

- **URL**: `/api/v1/user/edit/contact/{user_id}/`
- **Метод**: PATCH
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Тело запроса**:
  ```json
  {
    "name": "Иван Иванов",
    "phone": "+79001234567",
    "email": "ivan@example.com",
    "relationship": "Брат"
  }
  ```
  | Поле | Тип | Обязательное | Описание |
  |------|-----|--------------|----------|
  | name | string | Да | Имя контактного лица |
  | phone | string | Да | Телефон контактного лица |
  | email | string | Нет | Email контактного лица |
  | relationship | string | Да | Кем приходится пользователю |

- **Ответ**:
  - Успех (201 Created):
    ```json
    {
      "message": "A new emergency contact has been created.",
      "data": {
        "id": 1,
        "name": "Иван Иванов",
        "phone": "+79001234567",
        "email": "ivan@example.com",
        "relationship": "Брат"
      }
    }
    ```
  - Ошибка (400 Bad Request):
    ```json
    {
      "error": "The 'name', 'phone', and 'relationship' fields are required."
    }
    ```
  - Ошибка (403 Forbidden):
    ```json
    {
      "error": "You are not authorized to edit another user's emergency contact."
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X PATCH \
    http://127.0.0.1:8000/api/v1/user/edit/contact/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0' \
    -H 'Content-Type: application/json' \
    -d '{
      "name": "Иван Иванов",
      "phone": "+79001234567",
      "email": "ivan@example.com",
      "relationship": "Брат"
    }'
  ```

### Создание контакта терапевта
Создает новый контакт терапевта для пользователя.

- **URL**: `/api/v1/user/create/therapist/{user_id}/`
- **Метод**: PUT
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Тело запроса**:
  ```json
  {
    "name": "Петр Петров",
    "phone": "+79001234567",
    "email": "petr@example.com"
  }
  ```
  | Поле | Тип | Обязательное | Описание |
  |------|-----|--------------|----------|
  | name | string | Да | Имя терапевта |
  | phone | string | Да | Телефон терапевта |
  | email | string | Да | Email терапевта |

- **Ответ**:
  - Успех (201 Created):
    ```json
    {
      "message": "A new therapist contact has been created.",
      "data": {
        "id": 1,
        "name": "Петр Петров",
        "phone": "+79001234567",
        "email": "petr@example.com"
      }
    }
    ```
  - Ошибка (403 Forbidden):
    ```json
    {
      "error": "You are not authorized to edit another user's therapist contact."
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X PUT \
    http://127.0.0.1:8000/api/v1/user/create/therapist/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0' \
    -H 'Content-Type: application/json' \
    -d '{
      "name": "Петр Петров",
      "phone": "+79001234567",
      "email": "petr@example.com"
    }'
  ```

### Редактирование контакта терапевта
Обновляет существующий контакт терапевта для пользователя.

- **URL**: `/api/v1/user/edit/therapist/{user_id}/`
- **Метод**: PATCH
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Тело запроса**:
  ```json
  {
    "name": "Петр Петров",
    "phone": "+79001234567",
    "email": "petr@example.com"
  }
  ```
  | Поле | Тип | Обязательное | Описание |
  |------|-----|--------------|----------|
  | name | string | Нет | Имя терапевта |
  | phone | string | Нет | Телефон терапевта |
  | email | string | Нет | Email терапевта |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "message": "Therapist contact has been updated.",
      "data": {
        "id": 1,
        "name": "Петр Петров",
        "phone": "+79001234567",
        "email": "petr@example.com"
      }
    }
    ```
  - Ошибка (403 Forbidden):
    ```json
    {
      "error": "You are not authorized to edit another user's therapist contact."
    }
    ```
  - Ошибка (404 Not Found):
    ```json
    {
      "error": "Therapist contact not found for this user."
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X PATCH \
    http://127.0.0.1:8000/api/v1/user/edit/therapist/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0' \
    -H 'Content-Type: application/json' \
    -d '{
      "name": "Петр Петров",
      "phone": "+79001234567",
      "email": "petr@example.com"
    }'
  ```

### Получение списка музыкальных треков
Возвращает список доступных музыкальных треков для терапии.

- **URL**: `/api/v1/user/music/`
- **Метод**: GET
- **Аутентификация**: Требуется

- **Ответ**:
  - Успех (200 OK):
    ```json
    [
      {
        "id": 1,
        "name": "Спокойный океан",
        "url": "https://example.com/music/ocean.mp3"
      },
      {
        "id": 2,
        "name": "Лесные звуки",
        "url": "https://example.com/music/forest.mp3"
      }
    ]
    ```
    | Поле | Тип | Описание |
    |------|-----|----------|
    | id | integer | ID музыкального трека |
    | name | string | Название трека |
    | url | string | URL для воспроизведения трека |

- **Пример запроса**:
  ```bash
  curl -X GET \
    http://127.0.0.1:8000/api/v1/user/music/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0'
  ```

### Установка музыкального трека для пользователя
Устанавливает выбранный музыкальный трек для пользователя.

- **URL**: `/api/v1/user/music/edit/{user_id}/`
- **Метод**: POST
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Тело запроса**:
  ```json
  {
    "music": 2
  }
  ```
  | Поле | Тип | Обязательное | Описание |
  |------|-----|--------------|----------|
  | music | integer | Да | ID музыкального трека |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "message": "Music track updated successfully"
    }
    ```
  - Ошибка (404 Not Found):
    ```json
    {
      "error": "Music track not found"
    }
    ```
  - Ошибка (400 Bad Request):
    ```json
    {
      "error": "Music ID is required"
    }
    ```
  - Ошибка (403 Forbidden):
    ```json
    {
      "error": "You are not authorized to edit this user's music preferences."
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X POST \
    http://127.0.0.1:8000/api/v1/user/music/edit/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0' \
    -H 'Content-Type: application/json' \
    -d '{
      "music": 2
    }'
  ```

## API событий

### Активация тревоги
Активирует сценарий тревоги для пользователя, который может включать воспроизведение музыки, отправку уведомлений контактам и терапевту.

- **URL**: `/api/v1/event/trigger/{user_id}/`
- **Метод**: GET
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "scenario": "Стандартный сценарий",
      "play_music": true,
      "messages": [
        "Ваш/ваша Брат (Иван Иванов) получил(а) уведомление по email.",
        "Ваш психотерапевт (Петр Петров) был уведомлён."
      ]
    }
    ```
    | Поле | Тип | Описание |
    |------|-----|----------|
    | scenario | string | Название активированного сценария |
    | play_music | boolean | Флаг, указывающий, нужно ли воспроизводить музыку (функциональность перенесена на фронтенд) |
    | messages | array | Список сообщений о выполненных действиях |

  - Ошибка (404 Not Found):
    ```json
    {
      "error": "User or UserInfo not found"
    }
    ```
  - Ошибка (404 Not Found):
    ```json
    {
      "error": "No AlarmScenario associated with this user"
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X GET \
    http://127.0.0.1:8000/api/v1/event/trigger/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0'
  ```

## API чата

### Отправка сообщения GPT
Отправляет сообщение GPT-ассистенту и получает ответ.

- **URL**: `/api/v1/chat/{user_id}/`
- **Метод**: POST
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Тело запроса**:
  ```json
  {
    "text": "Как справиться с тревогой?"
  }
  ```
  | Поле | Тип | Обязательное | Описание |
  |------|-----|--------------|----------|
  | text | string | Да | Текст сообщения для GPT |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "response": "Для справления с тревогой можно использовать несколько методов: глубокое дыхание, медитация, физические упражнения. Также важно обратиться к специалисту для профессиональной помощи."
    }
    ```
  - Ошибка (400 Bad Request):
    ```json
    {
      "error": "Message text is required"
    }
    ```
  - Ошибка (403 Forbidden):
    ```json
    {
      "error": "You are not authorized to send messages to this user"
    }
    ```
  - Ошибка (404 Not Found):
    ```json
    {
      "error": "User not found"
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X POST \
    http://127.0.0.1:8000/api/v1/chat/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0' \
    -H 'Content-Type: application/json' \
    -d '{
      "text": "Как справиться с тревогой?"
    }'
  ```

### Получение URL для WebSocket чата поддержки
Возвращает URL для подключения к WebSocket чату поддержки.

- **URL**: `/api/v1/chat/user/support/{user_id}/`
- **Метод**: GET
- **Аутентификация**: Требуется
- **Параметры URL**:
  | Параметр | Тип | Описание |
  |----------|-----|----------|
  | user_id | integer | ID пользователя |

- **Ответ**:
  - Успех (200 OK):
    ```json
    {
      "user_id": 1,
      "is_admin": false,
      "websocket_url": "ws://127.0.0.1:8000/ws/chat/1/"
    }
    ```
    | Поле | Тип | Описание |
    |------|-----|----------|
    | user_id | integer | ID пользователя |
    | is_admin | boolean | Флаг, указывающий, является ли пользователь администратором |
    | websocket_url | string | URL для подключения к WebSocket |

  - Ошибка (403 Forbidden):
    ```json
    {
      "error": "You are not authorized to access this chat"
    }
    ```
  - Ошибка (404 Not Found):
    ```json
    {
      "error": "User not found"
    }
    ```

- **Пример запроса**:
  ```bash
  curl -X GET \
    http://127.0.0.1:8000/api/v1/chat/user/support/1/ \
    -H 'Authorization: Token a1b2c3d4e5f6g7h8i9j0'
  ```

## WebSocket соединения

### Чат поддержки
WebSocket соединение для чата поддержки между пользователем и администратором.

- **URL**: `ws://127.0.0.1:8000/ws/chat/{user_id}/`
- **Аутентификация**: Токен требуется в параметрах соединения

#### Формат сообщений от клиента к серверу
```json
{
  "message": "Мне нужна помощь с приложением"
}
```
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| message | string | Да | Текст сообщения |

#### Формат сообщений от сервера к клиенту
```json
{
  "event": "chat_message",
  "message": "Чем я могу вам помочь?",
  "identifier": "1",
  "user_id": "1",
  "from_admin": true
}
```
| Поле | Тип | Описание |
|------|-----|----------|
| event | string | Тип события ("chat_message", "user_connected", "user_disconnected") |
| message | string | Текст сообщения |
| identifier | string | Идентификатор пользователя или сессии |
| user_id | string | ID пользователя |
| from_admin | boolean | Флаг, указывающий, что сообщение от администратора |

#### События WebSocket
1. **chat_message**: Получение сообщения
2. **user_connected**: Уведомление о подключении пользователя (только для админов)
3. **user_disconnected**: Уведомление об отключении пользователя (только для админов)

#### Пример использования WebSocket (JavaScript)
```javascript
// Подключение к WebSocket
const socket = new WebSocket('ws://127.0.0.1:8000/ws/chat/1/');

// Обработка открытия соединения
socket.onopen = function(e) {
  console.log('Соединение установлено');
};

// Обработка входящих сообщений
socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Получено сообщение:', data);

  if (data.event === 'chat_message') {
    // Отображение сообщения в интерфейсе
    displayMessage(data.message, data.from_admin);
  }
};

// Отправка сообщения
function sendMessage(message) {
  socket.send(JSON.stringify({
    'message': message
  }));
}

// Обработка ошибок
socket.onerror = function(error) {
  console.log('Ошибка WebSocket:', error);
};

// Обработка закрытия соединения
socket.onclose = function(event) {
  console.log('Соединение закрыто');
};
```

### Административный чат
WebSocket соединение для администраторов, позволяющее отвечать на сообщения пользователей.

- **URL**: `ws://127.0.0.1:8000/ws/chat/admin/`
- **Аутентификация**: Требуется (только для администраторов)

#### Формат сообщений от админа к серверу
```json
{
  "message": "Чем я могу вам помочь?",
  "user_id": "1"
}
```
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| message | string | Да | Текст сообщения |
| user_id | string | Да | ID пользователя, которому отправляется сообщение |

#### Формат сообщений от сервера к админу
```json
{
  "event": "chat_message",
  "message": "Мне нужна помощь с приложением",
  "identifier": "1",
  "user_id": "1"
}
```
| Поле | Тип | Описание |
|------|-----|----------|
| event | string | Тип события ("chat_message", "user_connected", "user_disconnected") |
| message | string | Текст сообщения |
| identifier | string | Идентификатор пользователя или сессии |
| user_id | string | ID пользователя |

## Модели данных

### Пользователь (User)
Стандартная модель пользователя Django с полями:
- username: Имя пользователя
- email: Email пользователя
- password: Пароль пользователя (хранится в зашифрованном виде)

### Информация о пользователе (UserInfo)
- user: Связь с моделью User (один к одному)
- age: Возраст пользователя
- location: Местоположение пользователя
- military_status: Военный статус (true/false)
- ptsd_level: Уровень ПТСР (1-5)
- music: Связь с моделью MusicTrack
- therapist_contact: Связь с моделью Therapist
- scenario: Связь с моделью AlarmScenario

### Экстренный контакт (EmergencyContact)
- user: Связь с моделью User (многие к одному)
- name: Имя контактного лица
- relationship: Кем приходится пользователю
- phone: Телефон контактного лица
- email: Email контактного лица

### Музыкальный трек (MusicTrack)
- name: Название трека
- url: URL для воспроизведения трека

### Терапевт (Therapist)
- user: Связь с моделью User (один к одному)
- name: Имя терапевта
- phone: Телефон терапевта
- email: Email терапевта

### Сценарий тревоги (AlarmScenario)
- name: Название сценария
- play_music: Флаг воспроизведения музыки
- notify_contact: Флаг уведомления контактов
- notify_therapist: Флаг уведомления терапевта

### Тревога (Alarm)
- user: Связь с моделью User (многие к одному)
- scenario: Связь с моделью AlarmScenario (многие к одному)
- timestamp: Время создания тревоги

### Результат тревоги (AlarmResult)
- alarm: Связь с моделью Alarm (один к одному)
- location: Местоположение во время тревоги
- timestamp: Время создания результата
- music_played: Флаг воспроизведения музыки
- message_sent_to_contacts: Флаг отправки сообщения контактам
- voice_message_played: Флаг воспроизведения голосового сообщения
- therapist_notified: Флаг уведомления терапевта
- completed: Флаг завершения тревоги

### Сессия чата (ChatSession)
- user: Связь с моделью User (многие к одному)
- session_type: Тип сессии ('gpt' или 'user')
- receiver: Связь с моделью User (получатель, если чат с пользователем)
- started_at: Время начала сессии
- ended_at: Время окончания сессии

### Сообщение чата (ChatMessage)
- session: Связь с моделью ChatSession (многие к одному)
- sender: Тип отправителя ('user', 'gpt', 'system')
- message: Текст сообщения
- timestamp: Время отправки сообщения
