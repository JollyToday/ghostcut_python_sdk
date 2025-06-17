from pydantic import BaseModel, Field


class ErrorInfo(BaseModel):
    trace_id: str = Field(..., description="trace id")
    error: str = Field(..., description="error code")
