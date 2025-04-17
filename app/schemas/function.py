from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from app.models.function import Language, Runtime

class FunctionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1)
    language: Language
    timeout: Optional[int] = Field(30, ge=1, le=300)
    memory_limit: Optional[int] = Field(128, ge=64, le=1024)
    runtime: Optional[Runtime] = Field(Runtime.DOCKER)

class FunctionCreate(FunctionBase):
    pass

class FunctionUpdate(FunctionBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1)
    language: Optional[Language] = None
    timeout: Optional[int] = Field(None, ge=1, le=300)
    memory_limit: Optional[int] = Field(None, ge=64, le=1024)
    runtime: Optional[Runtime] = None

class Function(FunctionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class FunctionExecute(BaseModel):
    input: Any
