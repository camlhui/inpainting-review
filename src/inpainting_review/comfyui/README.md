# Programmatic Usage of ComfyUI

ComfyUI is a powerful tool for building and managing workflows in generative image tasks. Its intuitive user interface excels at creating, inspecting, and quickly prototyping workflows. However, when workflows are finalized and need to be used extensively—especially for batch processing or remote server operations a programmatic approach becomes more efficient.

To simplify and streamline these operations, we have built a Python module that wraps the ComfyUI API and provides a convenient [CLI](comfy2py.py) tool.

This tool simply require users to export workflows as JSON specifications (using API export functionality of the UI) to be submitted programmatically to ComfyUI server through the CLI. Additioanally those workflow specifications can be version-controlling to track changes.

# Programmatic usage of ComfyUI


## Setup

As part of this benchmark, inpainting workflows were run on Google Colab using NVIDIA A100 GPUs. Below are instructions to set up and execute these workflows.

>[comfyui_installation.ipynb](../../../notebooks/comfyui_installation.ipynb)

### Install ComfyUI

ComfyUI can be installed on Google Drive storage, which is mounted to Colab VMs. For ease of use, it's recommended to install ComfyUI using the ComfyUI Manager, as it simplifies adding or upgrading modules (e.g., custom nodes).

For additional information refer to the installation guide
 https://github.com/ltdrdata/ComfyUI-Manager/blob/main/notebooks/comfyui_colab_with_manager.ipynb.

### Download models

Download the necessary models and organize them within the ComfyUI file structure as outlined in the installation notebooks or tutorials.


### Install `inpainting_review` package

The `inpainting_review` package is required to run the workflows and interact with ComfyUI programmatically.

You can install it with the following commands

```shell
!git clone https://github.com/camlhui/inpainting-review.git

!cd /content/inpainting-review/

!pip install .
```


## Workflow execution

A full demo example is given in [comfyui_execution.ipynb](../../../notebooks/comfyui_execution.ipynb)

1. Start the ComfyUI Server

Starts the ComfyUI server and opens a Cloudflared tunnel to enable UI access (the URL gets printed when available).

```shell
comfy2py start
```


2. Run a workflow

Submits a workflow and track its execution. This command is synchronous.

```shell
comfy2py run <name> <image_path> <mask_path> <output_path> [options]
```
Arguments:

- `<name>`: The name of the inpainting workflow to use (should match the name of one of the [workflow JSON files](workflows/))
- `<image_path>`: Path to the input image file.
- `<mask_path>`: Path to the mask image file.
- `<output_path>`: Path where the output image should be saved.

Options:
- `--prompt` (default: ""): A positive prompt describing the desired outcome.
- `--neg-prompt` (default: ""): A negative prompt specifying aspects to avoid in the result.
- `--steps` (default: 50): Number of denoising steps for the workflow.
- `--timeout` (default: 1800): Maximum time (in seconds) to wait for the workflow to complete.

3. Flush GPU memory (optional)

```bash
comfy2py flush
```

4. Stop the server

```bash
comfy2py stop
```

>Note: all those commands can also be executed as python commands
```python comfy2py.py command args --option```
