from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class BaseIdModel(SQLModel):
    id: str | None = Field(default_factory=lambda: uuid.uuid4().hex, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.now}
    )