import json
import os
from typing import Optional


from app.comfyui.utils import (
    retrieve_output_file,
    submit_workflow,
    update_workflow_parameters,
    copy_inputs,
    wait_for_workflow_completion,
)


INPAINTING_WOKFLOWS = {"flux-1-fill-dev", "stable-diffusion-2-inpainting"}


def run_workflow(
    name: str,
    image_path: str,
    mask_path: str,
    output_path: str,
    prompt: str,
    neg_prompt: Optional[str] = None,
    steps: Optional[int] = None,
    timeout: int = 1800,
):
    if name not in INPAINTING_WOKFLOWS:
        raise ValueError(
            f"Invalid workflow name: {name}. Available workflows: {', '.join(INPAINTING_WOKFLOWS)}"  # noqa: E501
        )

    filepath = os.path.join(os.path.dirname(__file__), "workflows", f"{name}.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Workflow file not found: {filepath}")

    with open(filepath, "r") as f:
        workflow = json.load(f)

    update_workflow_parameters(
        workflow,
        image_path=image_path,
        mask_path=mask_path,
        prompt=prompt,
        neg_prompt=neg_prompt,
        steps=steps,
    )

    copy_inputs(image_path=image_path, mask_path=mask_path)

    workflow_id = submit_workflow(workflow=workflow)
    completed_workflow = wait_for_workflow_completion(
        workflow_id=workflow_id, timeout=timeout
    )

    retrieve_output_file(completed_workflow=completed_workflow, output_path=output_path)
