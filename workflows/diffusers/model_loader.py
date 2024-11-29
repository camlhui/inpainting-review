import os
from typing import Dict
from diffusers import FluxFillPipeline, DiffusionPipeline
import torch

from task_definitions import Models
from workflows.utils import check_cuda_availability


assert os.environ.get(
    "HUGGING_FACE_HUB_TOKEN"
), "HUGGING_FACE_HUB_TOKEN is not set or is empty"

check_cuda_availability()


_model_cache: Dict[Models, DiffusionPipeline] = {}


def get_pipeline(model: Models):
    if model in _model_cache:
        return _model_cache[model]

    elif model == Models.FLUX_1_FILL_DEV:
        pipe = FluxFillPipeline.from_pretrained(
            Models.FLUX_1_FILL_DEV.value,
            torch_dtype=torch.bfloat16,
            cache_dir=os.environ.get("HUGGING_FACE_CACHE_DIR"),
        ).to("cuda")
        _model_cache[model] = pipe
        return pipe

    raise ValueError(f"Unknown model name, model: {model}")
