from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class BaseIdModel(SQLModel):
    id: int | None = Field(default=uuid.uuid4().hex, index=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.now}
    )