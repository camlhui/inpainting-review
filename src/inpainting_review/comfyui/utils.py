import json
import os
import random
import shutil
import time
from typing import Optional

import requests


def update_workflow_parameters(
    workflow: dict,
    image_path: str,
    mask_path: str,
    prompt: str,
    neg_prompt: Optional[str] = None,
    steps: Optional[int] = None,
):
    for node_id, node in workflow.items():
        class_type = node.get("class_type")

        # Update seed and steps
        if class_type == "KSampler":
            node["inputs"]["steps"] = steps if steps else node["inputs"]["steps"]
            node["inputs"]["seed"] = random.randint(0, 2**64)

        # Update image and mask filenames
        if class_type == "LoadImage" and node["inputs"]["upload"] == "image":
            node["inputs"]["image"] = os.path.basename(image_path)

        if class_type == "LoadImageMask" and node["inputs"]["upload"] == "image":
            node["inputs"]["image"] = os.path.basename(mask_path)

        # Update output filename prefix
        if class_type == "SaveImage":
            filename = os.path.basename(mask_path)
            filename_without_ext = os.path.splitext(filename)[0]
            node["inputs"]["filename_prefix"] = filename_without_ext

        # Update prompts
        if class_type == "CLIPTextEncode":
            if "Positive Prompt" in node["_meta"]["title"]:
                node["inputs"]["text"] = prompt
            elif "Negative Prompt" in node["_meta"]["title"]:
                node["inputs"]["text"] = (
                    neg_prompt if neg_prompt else node["inputs"]["text"]
                )


def copy_inputs(image_path: str, mask_path: str):
    assert os.environ.get(
        "COMFYUI_INSTALL_DIR"
    ), "Missing environment variable COMFYUI_INSTALL_DIR."
    comfyui_input_dir = os.path.join(os.environ["COMFYUI_INSTALL_DIR"], "input")
    shutil.copy(image_path, comfyui_input_dir)
    shutil.copy(mask_path, comfyui_input_dir)


def submit_workflow(workflow: dict) -> str:
    assert os.environ.get(
        "COMFYUI_API_URL"
    ), "Missing environment variable COMFYUI_API_URL."
    response = requests.post(
        f"{os.environ['COMFYUI_API_URL']}/api/prompt",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"prompt": workflow}).encode("utf-8"),
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to submit workflow: {response.text}")

    return response.json()["prompt_id"]


def wait_for_workflow_completion(workflow_id: str, timeout: int = 1800) -> dict:
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(f"Workflow execution timed out after {timeout} seconds.")

        queue_state = requests.get(f"{os.environ['COMFYUI_API_URL']}/api/queue").json()
        running_workflow_ids = {record[1] for record in queue_state["queue_running"]}
        pending_workflow_ids = {record[1] for record in queue_state["queue_pending"]}

        if not (
            workflow_id in running_workflow_ids or workflow_id in pending_workflow_ids
        ):
            reponse = requests.get(
                f"{os.environ['COMFYUI_API_URL']}/api/history/{workflow_id}"
            ).json()
            return list(reponse.values())[0]

        time.sleep(1)


def retrieve_output_file(completed_workflow: dict, output_path: str):
    if not completed_workflow["status"]["completed"]:
        raise RuntimeError(f"Workflow failed: {completed_workflow['status']}")

    images = list(completed_workflow["outputs"].values())[0]["images"]
    if len(images) != 1:
        raise ValueError("One output is expected per workflow.")

    output_filename = images[0]["filename"]
    comfyui_output_dir = os.path.join(os.environ["COMFYUI_INSTALL_DIR"], "output")
    comfyui_output_file = os.path.join(comfyui_output_dir, output_filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    shutil.copy(comfyui_output_file, output_path)
