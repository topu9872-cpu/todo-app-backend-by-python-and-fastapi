from fastapi import APIRouter

from app.database import todo_collection
from app.schema import TodoCreate
from fastapi import FastAPI
router = APIRouter(tags=["Todos"])
app=FastAPI()

@router.post("/tasks")
async def create_todo(todo: TodoCreate):
    result = await todo_collection.insert_one(todo.model_dump())

    return {
        "message": "Todo created",
        "id": str(result.inserted_id)
    }

app.include_router(router)