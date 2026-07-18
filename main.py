from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Clean room", "done": False},
    {"id": 3, "title": "Finish assignment", "done": True},
]

class TaskCreate(BaseModel):
    title: str
    done: bool = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


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
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")  

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    new_id = max((task_item["id"] for task_item in tasks), default=0) + 1
    new_task = {"id": new_id, "title": task.title, "done": task.done}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: UpdateTask):
    for task in tasks:
        if task["id"] == task_id:
            if updated.title is not None:
                title = updated.title.strip()
                if not title:
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = title
            if updated.done is not None:
                task["done"] = updated.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Get a single task id than  delete a task"""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

