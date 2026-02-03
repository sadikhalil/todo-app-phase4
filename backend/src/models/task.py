from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..db.database import Base

# Define enum values for SQLAlchemy
TASK_STATUS_VALUES = ('incomplete', 'complete')
TASK_PRIORITY_VALUES = ('low', 'medium', 'high')
RECURRENCE_PATTERN_VALUES = ('daily', 'weekly', 'monthly')

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(*TASK_STATUS_VALUES), nullable=False, default='incomplete')
    priority = Column(SQLEnum(*TASK_PRIORITY_VALUES), nullable=True, default='medium')
    due_date = Column(DateTime(timezone=True), nullable=True)
    reminder_date = Column(DateTime(timezone=True), nullable=True)
    recurrence_pattern = Column(SQLEnum(*RECURRENCE_PATTERN_VALUES), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    # Relationship to user
    user = relationship("User", back_populates="tasks")