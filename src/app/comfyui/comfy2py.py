import click
from app.comfyui.server import (
    start as start_server,
    stop as stop_server,
    flush as flush_gpu_memory,
)
from app.comfyui.workflow import run_workflow


@click.group()
def cli():
    """confy2py: A CLI for managing ComfyUI workflows."""
    pass


@cli.command()
def start():
    """Start the ComfyUI server."""
    start_server()


@cli.command()
def stop():
    """Stop the ComfyUI server."""
    stop_server()


@cli.command()
def flush():
    """Flush GPU memory."""
    flush_gpu_memory()


@cli.command()
@click.argument("name")
@click.argument("image-path")
@click.argument("mask-path")
@click.argument("output-path")
@click.option("--prompt", default="", help="Positive prompt for the workflow.")
@click.option("--neg-prompt", default="", help="Negative prompt for the workflow.")
@click.option("--steps", default=50, help="Number of steps for the workflow.")
@click.option("--timeout", default=1800, help="Timeout for the workflow completion.")
def run(name, image_path, mask_path, output_path, prompt, neg_prompt, steps, timeout):
    """Run a ComfyUI workflow.

    NAME: Name of the inpainting workflow to use.
    IMAGE_PATH: Path to the input image file.
    MASK_PATH: Path to the mask image file.
    OUTPUT_PATH: Path to save the output image.
    """
    run_workflow(
        name=name,
        image_path=image_path,
        mask_path=mask_path,
        output_path=output_path,
        prompt=prompt,
        neg_prompt=neg_prompt,
        steps=steps,
        timeout=timeout,
    )


if __name__ == "__main__":
    cli()
