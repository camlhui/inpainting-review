import os
from typing import List

from models import InpaintingTask
from workflows.utils import set_hugging_face_hub_token, assert_cuda_availability

from diffusers import FluxFillPipeline
from diffusers.utils import load_image


set_hugging_face_hub_token()
assert os.environ.get(
    "HUGGING_FACE_HUB_TOKEN"
), "HUGGING_FACE_HUB_TOKEN is not set or is empty"

assert_cuda_availability()


def _get_pipeline():
    import torch

    pipe = FluxFillPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-Fill-dev",
        torch_dtype=torch.bfloat16,
        cache_dir=os.environ.get("HUGGING_FACE_CACHE_DIR"),
    ).to("cuda")

    return pipe


def run(tasks: List[InpaintingTask], output_dir: str):
    import torch

    pipe = _get_pipeline()

    for task in tasks:
        source_image = load_image(task.source_image)
        mask_image = load_image(task.mask_image).point(
            lambda x: 255 if x > 128 else 0, mode="1"
        )

    image = pipe(
        prompt=task.prompt,
        image=source_image,
        mask_image=mask_image,
        height=source_image.size[1],
        width=source_image.size[0],
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(0),
    ).images[0]

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{task['task_id']}.png")
    image.save(output_path)
