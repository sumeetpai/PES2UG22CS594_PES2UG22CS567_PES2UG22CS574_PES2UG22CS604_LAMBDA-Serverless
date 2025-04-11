from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.execution import FunctionExecutionEngine
from app.models.function import Function as FunctionModel
from app.schemas.function import Function, FunctionCreate, FunctionUpdate, FunctionExecute

router = APIRouter()
execution_engine = FunctionExecutionEngine()

@router.post("/", response_model=Function)
def create_function(function: FunctionCreate, db: Session = Depends(get_db)):
    db_function = FunctionModel(
        name=function.name,
        code=function.code,
        language=function.language,
        timeout=function.timeout,
        memory_limit=function.memory_limit,
        created_at=datetime.utcnow()
    )
    db.add(db_function)
    db.commit()
    db.refresh(db_function)
    return db_function

@router.get("/", response_model=List[Function])
def list_functions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    functions = db.query(FunctionModel).offset(skip).limit(limit).all()
    return functions

@router.get("/{function_id}", response_model=Function)
def get_function(function_id: int, db: Session = Depends(get_db)):
    function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    return function

@router.put("/{function_id}", response_model=Function)
def update_function(function_id: int, function: FunctionUpdate, db: Session = Depends(get_db)):
    db_function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if db_function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    
    update_data = function.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_function, key, value)
    
    db.commit()
    db.refresh(db_function)
    return db_function

@router.delete("/{function_id}")
def delete_function(function_id: int, db: Session = Depends(get_db)):
    function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    
    db.delete(function)
    db.commit()
    return {"message": "Function deleted successfully"}

@router.post("/{function_id}/execute")
def execute_function(function_id: int, input_data: FunctionExecute, db: Session = Depends(get_db)):
    function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    
    try:
        result = execution_engine.execute(
            function_id=function_id,
            code=function.code,
            language=function.language,
            input_data=input_data.input
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 