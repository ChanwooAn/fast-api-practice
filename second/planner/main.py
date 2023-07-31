import uvicorn
from fastapi import FastAPI

from planner.database.connection import Settings
from planner.routes.events import event_router
from planner.routes.users import user_router

app = FastAPI()
settings = Settings()
app.include_router(user_router, prefix="/user")
app.include_router(event_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
