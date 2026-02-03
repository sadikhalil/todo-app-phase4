from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    # Relationship to tasks
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")