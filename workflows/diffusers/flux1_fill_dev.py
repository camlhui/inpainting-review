from datetime import datetime
import os
import time
from typing import List

from task_definitions import InpaintingTask, Models
from workflows.diffusers.model_loader import get_pipeline
from workflows.utils import load_and_preprocess_image, load_and_preprocess_mask


def run(tasks: List[InpaintingTask], output_dir: str):
    import torch

    pipe = get_pipeline(model=Models.FLUX_1_FILL_DEV)

    data_dir = os.environ["DATA_DIR"]
    run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_dir = os.path.join(output_dir, run_timestamp)
    os.makedirs(output_dir, exist_ok=True)

    seed = int(time.time()) % 2**32
    generator = torch.Generator("cpu").manual_seed(seed)

    for task in tasks:
        image = load_and_preprocess_image(os.path.join(data_dir, task.source_image))
        mask = load_and_preprocess_mask(os.path.join(data_dir, task.mask_image))
        inpainted_image = pipe(
            prompt=task.prompt,
            image=image,
            mask_image=mask,
            height=image.size[1],
            width=image.size[0],
            max_sequence_length=512,
            generator=generator,
        ).images[0]

        output_path = os.path.join(output_dir, f"{task.task_id}.png")
        inpainted_image.save(output_path)
