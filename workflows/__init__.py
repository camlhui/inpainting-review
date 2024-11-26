import importlib
import os
from typing import List

from task_definitions import InpaintingTask, Models


def run_workflow(model: Models, tasks: List[InpaintingTask]):

    if model == Models.FLUX_1_FILL_DEV:
        workflow_module = importlib.import_module("workflows.flux_1_fill_dev")
        output_dir = os.path.join(os.environ["DATA_DIR"], model.value.replace("/", "_"))
        workflow_module.run(model=model, tasks=tasks, output_dir=output_dir)

    raise ValueError(f"Unknown model, model: {model.value}")
