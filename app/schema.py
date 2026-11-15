
from typing import List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):

  title: str
  description: str
  status: str
  priority:str
  dueDate: str
  progress:int
  tags:List[str]=0
  createdAt:str
  userId:str
  createdAt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )