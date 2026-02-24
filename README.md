# User Service Project

This repository contains a simple Flask-based web service for storing user information. The project is structured in a three-layer architecture:

- **Persistence layer** (`persistence/user_repository.py`): in-memory storage using a dictionary.
- **Business logic layer** (`services/user_service.py`): validation and data transformation.
- **Presentation layer** (`app`): Flask routes handling HTTP requests.

## Features

- GET `/users` - list all users
- GET `/users/<id>` - get specified user
- POST `/users` - create user
- PATCH `/users/<id>` - update user
- DELETE `/users/<id>` - delete user

Input JSON (create/patch):

```json
{
  "firstName": "str",
  "lastName": "str",
  "birthYear": 1980,
  "group": "user" // one of "user", "premium", "admin"
}
```

Output JSON:

```json
{
  "id": 1,
  "firstName": "str",
  "lastName": "str",
  "age": 41,
  "group": "user"
}
```

## Setup and run

```bash
python -m venv .venv
# activate environment
# on Windows PowerShell
.\.venv\Scripts\Activate
pip install -r requirements.txt
python run.py
```

## Testing

Unit and integration tests are located under `tests/`. To run all tests:

```bash
python -m pytest
```

## Notes

- The service uses HTTP/1.1 via Flask.
- Input validation returns 400 on bad data, 404 for missing users.
- Negative or zero IDs are treated as invalid.
- Age is computed from `birthYear` and current year.

```



```
