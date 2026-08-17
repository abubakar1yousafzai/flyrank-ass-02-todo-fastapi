from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import init_db, get_connection
import uvicorn


class TaskCreate(BaseModel):
    title: str
    done: bool = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

init_db()


app = FastAPI(
    title= "CRUD Todo",
    description="5 endpoint todo app",
    version="1.0.0"
)

@app.get("/")
def Home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    result = [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]

    return result

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Get a single task by its id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return {"id": row[0], "title": row[1], "done": bool(row[2])}

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Create a new task"""
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, task.done))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    result = {"id": new_id, "title": task.title, "done": task.done}

    return result

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: UpdateTask):
    """Get a single task id than update a task."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if updated.title is not None:
        new_title = updated.title.strip()
        if not new_title:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
    else:
        new_title = row[1]

    new_done = updated.done if updated.done is not None else bool(row[2])

    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?",(new_title, new_done, task_id ))
    conn.commit()
    conn.close()
    result = {"id": task_id, "title": new_title, "done": new_done}

    return result

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Get a single task id than  delete a task"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return Response(status_code=204)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
