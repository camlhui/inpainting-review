import os
from typing import List

from diffusers.utils import load_image

from task_definitions import InpaintingTask, Models
from workflows.model_loader import get_pipeline


def run(model: Models, tasks: List[InpaintingTask], output_dir: str):
    import torch

    pipe = get_pipeline(model)

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
