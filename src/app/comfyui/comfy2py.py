import argparse
from app.comfyui.server import (
    start as start_server,
    stop as stop_server,
    flush as flush_gpu_memory,
)
from app.comfyui.workflow import run_workflow


def start_command(args):
    """Start the ComfyUI server."""
    start_server()
    print("Server and tunnel started successfully.")


def stop_command(args):
    """Stop the ComfyUI server."""
    stop_server()
    print("Server stopped successfully.")


def flush_command(args):
    """Flush GPU memory."""
    flush_gpu_memory()
    print("GPU memory flushed successfully.")


def run_command(args):
    """Run a ComfyUI workflow."""
    run_workflow(
        name=args.name,
        image_path=args.image_path,
        mask_path=args.mask_path,
        output_path=args.output_path,
        prompt=args.prompt,
        neg_prompt=args.neg_prompt,
        steps=args.steps,
        timeout=args.timeout,
    )
    print("Workflow execution completed.")


def main():
    parser = argparse.ArgumentParser(
        description="confy2py: A CLI for managing ComfyUI workflows."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the ComfyUI server.")
    start_parser.set_defaults(func=start_command)

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop the ComfyUI server.")
    stop_parser.set_defaults(func=stop_command)

    # Flush command
    flush_parser = subparsers.add_parser("flush", help="Flush GPU memory.")
    flush_parser.set_defaults(func=flush_command)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a ComfyUI workflow.")
    run_parser.add_argument("name", help="Name of the inpainting workflow to use.")
    run_parser.add_argument("image_path", help="Path to the input image file.")
    run_parser.add_argument("mask_path", help="Path to the mask image file.")
    run_parser.add_argument("output_path", help="Path to save the output image.")
    run_parser.add_argument(
        "--prompt", default="", help="Positive prompt for the workflow."
    )
    run_parser.add_argument(
        "--neg-prompt", default="", help="Negative prompt for the workflow."
    )
    run_parser.add_argument(
        "--steps", type=int, default=50, help="Number of steps for the workflow."
    )
    run_parser.add_argument(
        "--timeout", type=int, default=1800, help="Timeout for the workflow completion."
    )
    run_parser.set_defaults(func=run_command)

    # Parse the arguments and call the appropriate function
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
