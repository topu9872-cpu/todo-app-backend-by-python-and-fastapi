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


from fastapi import Query

@router.get('/tasks')
async def get_todo(
    userId: str,
    search: str = "",
    page: int = 1,
    limit: int = 12
):
    query = {'userId': userId}

    # Search by title
    if search:
        query['title'] = {
            '$regex': search,
            '$options': 'i'
        }

    # Total matching tasks
    total = await todo_collection.count_documents(query)

    # Pagination
    skip = (page - 1) * limit

    result = await todo_collection.find(query) \
        .skip(skip) \
        .limit(limit) \
        .to_list(length=limit)

    for task in result:
        task['_id'] = str(task['_id'])

    return {
        'message': 'Tasks fetched successfully',
        'tasks': result,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'totalPages': (total + limit - 1) // limit
        }
    }