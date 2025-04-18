from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.execution import FunctionExecutionEngine
from app.models.function import Function as FunctionModel
from app.schemas.function import Function, FunctionCreate, FunctionUpdate, FunctionExecute
from app.models.metrics import ExecutionMetric  # <- Add this line

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
        runtime=function.runtime,
        created_at=datetime.utcnow()
    )
    db.add(db_function)
    db.commit()
    db.refresh(db_function)
    return db_function

@router.get("/", response_model=List[Function])
def list_functions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(FunctionModel).offset(skip).limit(limit).all()

@router.get("/{function_id}", response_model=Function)
def get_function(function_id: int, db: Session = Depends(get_db)):
    function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")
    return function

@router.put("/{function_id}", response_model=Function)
def update_function(function_id: int, function: FunctionUpdate, db: Session = Depends(get_db)):
    db_function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if not db_function:
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
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")
    db.delete(function)
    db.commit()
    return {"message": "Function deleted successfully"}

@router.post("/{function_id}/execute")
def execute_function(function_id: int, input_data: FunctionExecute, db: Session = Depends(get_db)):
    function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")

    try:
        result, metrics = execution_engine.execute(
            function_id=function.id,
            code=function.code,
            language=function.language,
            runtime=function.runtime,
            input_data=input_data.input
        )
        success = metrics.get("error") is None  # If no error, success is True

        db_metric = ExecutionMetric(
            function_id=function.id,
            execution_time=metrics["execution_time"],
            memory_used=metrics["memory_used"],
            success=success,
            error=metrics.get("error"),
            created_at=datetime.utcnow()
            )
        db.add(db_metric)
        db.commit()

        return {"result": result, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
