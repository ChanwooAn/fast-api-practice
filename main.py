from todo import todo_router
from fastapi import FastAPI

app=FastAPI()



@app.get("/")
async def say_hello() -> dict:
    return {
        "message": "Hello!"
    }

app.include_router(todo_router)
