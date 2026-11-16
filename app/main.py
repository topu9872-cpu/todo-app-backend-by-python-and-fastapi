import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.todo import router as todo_router

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
       os.getenv('NEXT_PUBLIC_URL')
    ],
    allow_credentials=True,
   
)

# Register Router
app.include_router(todo_router)


@app.get("/")
async def root():
    return {"message": "FastAPI Backend Running"}
