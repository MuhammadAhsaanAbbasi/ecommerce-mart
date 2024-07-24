from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class BaseIdModel(SQLModel):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.now}
    )