from enum import Enum
from typing import Optional

from pydantic import BaseModel


TARGET_RES = (1024, 1024)


class Models(Enum):
    FLUX_1_FILL_DEV = "black-forest-labs/FLUX.1-Fill-dev"


class InpaintingTask(BaseModel):
    task_id: str
    source_image: str
    mask_image: str
    prompt: str
    negative_prompt: Optional[str] = None
