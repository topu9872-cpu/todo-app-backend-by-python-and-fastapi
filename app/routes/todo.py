from app.database import todo_collection
from app.schema import TodoCreate
from fastapi import APIRouter, HTTPException
from fastapi import Query
from bson import ObjectId
router = APIRouter(tags=["Todos"])


@router.post("/tasks")
async def create_todo(todo: TodoCreate):
    result = await todo_collection.insert_one(todo.model_dump())
    print("post output result:", result)

    return {"message": "Todo created", "id": str(result.inserted_id)}


@router.get('/tasks')
async def get_all_todo(
    search: str,
    page: int,
    limit: int
):
    query = {}
    if search:
        query['title'] = {
            '$regex': search,
            '$options': 'i'
        }

    total = await todo_collection.count_documents(query)
    skip = (page-1)*limit
    result = (await todo_collection.find(query).skip(skip).limit(limit).to_list(length=limit))

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


@router.get('/tasks')
async def get_todo(
    userId: str,
    search: str,
    page: int,
    limit: int
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


@router.get('/tasks/{id}')
async def getTaskDetails(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail='Invalid task id'
        )
    result = await todo_collection.find_one({'_id': ObjectId(id)})
    if result is None:
        raise HTTPException(
            status_code=404,
            detail='task is not found'
        )

    result['_id'] = str(result['_id'])
    return {
        'success': True,
        ' message': 'task details get successfully',
        'task': result
    }


@router.delete('/tasks/{id}')
async def deleteTask(id:str):
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail='Invalid task id'
        )

    result = await todo_collection.find_one_and_delete({'_id': ObjectId(id)})
    if result is None:
        raise HTTPException(
            status_code=404,
            detail='task is not found'
        )
    return {
        'success': True,
        'message': 'task deleted successfully'
    }
