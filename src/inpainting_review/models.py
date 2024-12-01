from typing import Optional

from pydantic import BaseModel


class InpaintingTask(BaseModel):
    task_id: str
    source_image: str
    mask_image: str
    prompt: str
    negative_prompt: Optional[str] = None
