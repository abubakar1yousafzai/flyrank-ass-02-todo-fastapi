from fastapi import FastAPI

import uvicorn

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    