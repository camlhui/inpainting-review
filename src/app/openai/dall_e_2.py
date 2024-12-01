from datetime import datetime
import json
import os
from PIL import Image
from typing import List

from diffusers.utils import load_image
import openai

from app.models import InpaintingTask
from app.utils.image import (
    load_and_preprocess_image,
    load_and_preprocess_mask,
    image_to_bytes,
)

TARGET_RES = (1024, 1024)


assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY is not set or is empty"


def _create_openai_mask(image: Image, mask: Image) -> Image:
    """Convert a black and white mask to an image where the masked area is made
    transparent as expected by OpenAI edit API."""
    image = image.convert("RGBA")
    mask = mask.convert("L")
    alpha_mask = Image.eval(mask, lambda x: 255 - x)
    image.putalpha(alpha_mask)
    return image


def run(tasks: List[InpaintingTask]):
    assert os.environ.get("DATA_DIR"), "Missing environment variable DATA_DIR"
    data_dir = os.environ["DATA_DIR"]

    run_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_dir = os.path.join(
        os.environ["DATA_DIR"], "outputs", "dall-e-2", run_timestamp
    )
    os.makedirs(output_dir, exist_ok=True)

    for task in tasks:
        image = load_and_preprocess_image(os.path.join(data_dir, task.source_image))
        mask = load_and_preprocess_mask(os.path.join(data_dir, task.mask_image))
        openai_mask = _create_openai_mask(image, mask)

        response = openai.Image.create_edit(
            image=image_to_bytes(image),
            mask=image_to_bytes(openai_mask),
            prompt=task.prompt,
            n=1,
            size=f"{TARGET_RES[0]}x{TARGET_RES[1]}",
        )
        try:
            inpainted_image = load_image(response["data"][0]["url"])
        except Exception as e:
            raise RuntimeError(
                "An error occurred while processing the OpenAI API response"
            ) from e

        output_path = os.path.join(output_dir, f"{task.task_id}.png")
        inpainted_image.save(output_path)


if __name__ == "__main__":
    with open("../task-config.json") as f:
        tasks = json.load(f)["tasks"]

    run(tasks)
