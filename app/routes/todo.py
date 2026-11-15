from app.database import todo_collection
from app.schema import TodoCreate
from fastapi import APIRouter, HTTPException

# শুধু রাউটার ডিক্লেয়ার করা হবে
router = APIRouter(tags=["Todos"])

@router.post("/tasks")
async def create_todo(todo: TodoCreate):
  result = await todo_collection.insert_one(todo.model_dump())
  print("post output result:", result)

  return {"message": "Todo created", "id": str(result.inserted_id)}