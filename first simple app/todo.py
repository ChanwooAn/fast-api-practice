from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo", status_code=211)  # 성공 했을 때 코드 211로 설정
async def add_todo(todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully"
    }


@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list
    }


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied Id doesn't exist"
    ) # exception 발생시키기


@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="The Id of the todo to be updated")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "Todo updated successfully"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied Id doesn't exist"
    )


@todo_router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int = Path(..., title="the id of todo to be deleted")) -> dict:
    message = "Todo with supplied Id doesn't exist"
    for index in reversed(range(len(todo_list))):
        if todo_id == todo_list[index].id:
            todo_list.pop(index)
            return {
                "message": message
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied Id doesn't exist"
    )
