# models/metrics.py
from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class ExecutionMetric(Base):
    __tablename__ = "function_execution_metrics"

    id = Column(Integer, primary_key=True, index=True)
    function_id = Column(Integer, ForeignKey("functions.id", ondelete="CASCADE"))
    execution_time = Column(Float)  # In milliseconds
    success = Column(Boolean)
    memory_used = Column(Float)  # In megabytes, optional if available
    created_at = Column(DateTime, default=datetime.utcnow)
    error = Column(String, nullable=True)  # Add this if you want to track errors

    function = relationship("Function", back_populates="metrics")
