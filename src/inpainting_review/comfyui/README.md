
# TODO

As part of this benchmark exercise inpainting workflows were run with ComfyUI on Google Colab using a NVIDIA A100 GPU backend. Instructions are given below to run those workflows yourself.


## Setup

### Install ComfyUI

It's best to install ComfyUI with ComfyUI manager. As part of this benchmark we have installed it on Google Drive and used it from Google Colab.

Installation instructions are provided in https://github.com/ltdrdata/ComfyUI-Manager/blob/main/notebooks/comfyui_colab_with_manager.ipynb.

### Pytorch

```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Download models

###

## Workflow execution

In this repository we are providing a CLI to operate ComfyUI in a programmatic manner. It's built on top of ComfyUI API and can be used parallely to the Web UI.
