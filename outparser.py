from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict

class Metrics(BaseModel):
    metrics: Dict[str, str] = Field(description="7 metrics as keys and their values within 1-10")

class Options(BaseModel):
    options: Dict[str, str] = Field(description="3 career options as keys and the reason for choosing them")