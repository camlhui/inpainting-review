import argparse
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


def _submit_inpainting_workflow(
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

    filepath = f"./workflows/{name}.json"
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


def submit():
    parser = argparse.ArgumentParser(
        description="Submit an inpainting workflow for processing."
    )
    parser.add_argument(
        "name", type=str, help="Name of the inpainting workflow to use."
    )
    parser.add_argument("image_path", type=str, help="Path to the input image file.")
    parser.add_argument("mask_path", type=str, help="Path to the mask image file.")
    parser.add_argument("output_path", type=str, help="Path to save the output image.")
    parser.add_argument(
        "--prompt", type=str, default="", help="Positive prompt for the workflow."
    )
    parser.add_argument(
        "--neg_prompt", type=str, default="", help="Negative prompt for the workflow."
    )
    parser.add_argument(
        "--steps", type=int, default=None, help="Number of steps for the workflow."
    )
    parser.add_argument(
        "--timeout", type=int, default=1800, help="Timeout for the workflow completion."
    )

    args = parser.parse_args()

    _submit_inpainting_workflow(
        name=args.name,
        image_path=args.image_path,
        mask_path=args.mask_path,
        output_path=args.output_path,
        prompt=args.prompt,
        neg_prompt=args.neg_prompt,
        steps=args.steps,
        timeout=args.timeout,
    )
