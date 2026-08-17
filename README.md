# CRUD Todo API — SQLite Edition

A CRUD Todo API built with **FastAPI**, now backed by a real **SQLite** database instead of an in-memory list. This is the Week 3 continuation (Assignment BE-02) of the Week 2 CRUD API — the endpoints, request/response shapes, and validation rules are unchanged; only the storage layer was replaced.

## Why SQLite

SQLite was chosen because it requires no separate database server or installation — it stores the entire database in a single local file (`tasks.db`) and is built into Python's standard library via the `sqlite3` module. This makes it ideal for learning how an API talks to a real database before moving on to a client-server database like PostgreSQL.

## What Changed From the In-Memory Version

| Before (Week 2) | Now (Week 3) |
|---|---|
| Tasks stored in a Python list | Tasks stored in a SQLite database (`tasks.db`) |
| Data lost on every restart | Data persists across restarts |
| List loops to find/update/delete | SQL queries (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) |

The API's URLs, request bodies, and responses did not change — only the implementation behind each endpoint did.

## Where the Database Lives

The database is a single file, `tasks.db`, created automatically in the project's root folder the first time the app runs. It is **not committed to GitHub** (see `.gitignore`) — every clone of this repo generates its own fresh copy on first run.

## How to Install & Run

**Requirements:** Python 3.10+

1. Clone this repository:
   ```bash
   git clone https://github.com/abubakar1yousafzai/flyrank-ass-02-todo-fastapi
   cd flyrank-ass-02-todo-fastapi
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

3. Run the server:
   ```bash
   python main.py
   ```

4. On first run, `tasks.db` is created automatically, the `tasks` table is created, and 3 example tasks are seeded. On every later run, the existing data is reused — the seed only happens when the table is empty.

5. The API runs at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path             | Description                          | Success Status | Error Status |
|--------|------------------|---------------------------------------|-----------------|--------------|
| GET    | `/`              | API info (name, version, endpoints)   | 200             | —            |
| GET    | `/health`        | Health check                          | 200             | —            |
| GET    | `/tasks`         | List all tasks                        | 200             | —            |
| GET    | `/tasks/{id}`    | Get a single task by id                | 200             | 404          |
| POST   | `/tasks`         | Create a new task                     | 201             | 400          |
| PUT    | `/tasks/{id}`    | Update a task's title and/or done      | 200             | 400, 404     |
| DELETE | `/tasks/{id}`    | Delete a task                         | 204             | 404          |

## Example Request

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy eggs"}'
```

**Response:**
```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy eggs","done":false}
```

## Validation Rules

- `POST /tasks` and `PUT /tasks/{id}` reject an empty or missing `title` with a `400` error.
- Requesting or modifying a task id that doesn't exist returns a `404` error with a JSON message.

## Proving Persistence

To confirm data survives a restart:
1. Created several tasks via `POST /tasks`.
2. Stopped the server (`Ctrl+C`) and started it again (`python main.py`).
3. Ran `GET /tasks` again — all previously created tasks were still present, along with the original 3 seed tasks (which were not duplicated, since seeding only happens when the table is empty).

## Exploring the Database Directly (Stage 4)

The database was opened with **DB Browser for SQLite** to run queries directly against `tasks.db`, independent of the API:

```sql
SELECT * FROM tasks;
SELECT * FROM tasks WHERE done = 1;
SELECT COUNT(*) FROM tasks;
```

Changes made directly in the database viewer (e.g. marking a task as done) were immediately reflected when calling `GET /tasks` through the API — confirming that the API reads live from the same `tasks.db` file rather than any cached or hardcoded data.


## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (request validation)
- SQLite (`sqlite3`, Python standard library)

## Project Structure

```
.
├── main.py         # FastAPI app and routes
├── database.py     # SQLite connection, table creation, and seeding
├── tasks.db         # generated automatically, not committed
└── README.md
```