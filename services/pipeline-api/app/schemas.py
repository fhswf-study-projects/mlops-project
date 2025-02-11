from datetime import datetime
from typing import List, Optional


from pydantic import BaseModel, Field


class TestResponse(BaseModel):
    file_type: str
    filename: str