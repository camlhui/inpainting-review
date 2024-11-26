import json
import os
import textwrap
from typing import List

import matplotlib
import matplotlib.pyplot as plt

from task_definitions import InpaintingTask


def plot_tasks(tasks: List[InpaintingTask], output_path: str):
    matplotlib.use("Agg")  # use a non-interactive backend

    fig, axes = plt.subplots(nrows=len(tasks), ncols=3, figsize=(15, 5 * len(tasks)))

    for i, task in enumerate(tasks):
        source_img = plt.imread(task["source_image"])
        axes[i, 0].imshow(source_img)
        axes[i, 0].axis("off")
        axes[i, 0].set_title("Source Image")

        mask_img = plt.imread(task["mask_image"])
        axes[i, 1].imshow(mask_img)
        axes[i, 1].axis("off")
        axes[i, 1].set_title("Mask Image")

        wrapped_prompt = textwrap.fill(task["prompt"], width=50)
        axes[i, 2].text(0.5, 0.5, wrapped_prompt, ha="center", va="center", wrap=True)
        axes[i, 2].axis("off")
        axes[i, 2].set_title("Prompt")

    plt.tight_layout()

    fig.savefig(output_path)


if __name__ == "__main__":
    with open("task-config.json") as f:
        tasks = json.load(f)["tasks"]

    output_path = os.path.join(os.environ["DATA_DIR"], "outputs/benchmark.png")
    plot_tasks(tasks, output_path)
