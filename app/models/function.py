from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class Language(str, enum.Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"

class Runtime(str, enum.Enum):
    DOCKER = "docker"
    GVISOR = "gvisor"

class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    code = Column(String(4096))
    language = Column(Enum(Language))
    timeout = Column(Integer, default=30)
    memory_limit = Column(Integer, default=128)
    runtime = Column(Enum(Runtime), default=Runtime.DOCKER)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # NEW: Relationship to metrics
    metrics = relationship("ExecutionMetric", back_populates="function", cascade="all, delete-orphan")
