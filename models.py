from enum import Enum
from pydantic import BaseModel, Field

class ActionType(str, Enum):
    GOTO = "GOTO"
    CLICK = "CLICK"
    TYPE = "TYPE"
    WAIT_FOR = "WAIT_FOR"
    SCRAPE_TEXT = "SCRAPE_TEXT"

class DOMAction(BaseModel):
    action: ActionType
    selector: str | None = None
    value: str | None = None
    timeout_ms: int = Field(default=5000, description="Timeout for this specific action in ms")

class ExecutionRequest(BaseModel):
    url: str
    actions: list[DOMAction]
    return_selector: str = Field(..., description="DOM selector to extract final response text from")

class ExecutionResponse(BaseModel):
    status: str = Field(..., description="Status: 'success' or 'error'")
    scraped_data: str | None = None
    execution_time_ms: float
    error_message: str | None = None
