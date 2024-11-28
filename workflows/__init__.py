import importlib
import os
import sys
from typing import List

from task_definitions import InpaintingTask, Models


def _get_worfklow_module_name(model: Models) -> str:
    if model == Models.DALL_E_2:
        module_name = "workflows.dall_e_2"
    elif model == Models.FLUX_1_FILL_DEV:
        module_name = "workflows.flux1_fill_dev"
    else:
        raise ValueError(f"Unknown model, model: {model.value}")

    return module_name


def run_workflow(model: Models, tasks: List[InpaintingTask]):
    module_name = _get_worfklow_module_name(model)

    if module_name in sys.modules:
        workflow_module = sys.modules[module_name]
        importlib.reload(workflow_module)
    else:
        workflow_module = importlib.import_module(module_name)

    output_dir = os.path.join(
        os.environ["DATA_DIR"], "outputs", model.value.replace("/", "_")
    )
    workflow_module.run(model=model, tasks=tasks, output_dir=output_dir)
