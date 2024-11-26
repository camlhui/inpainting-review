import argparse
import json
import os
from workflows import load_workflow


def main():
    parser = argparse.ArgumentParser(description="Run inpainting workflows.")
    parser.add_argument("--workflow", required=True, help="Workflow name to execute.")
    parser.add_argument(
        "--output", default="data/outputs", help="Directory to save outputs."
    )
    args = parser.parse_args()

    with open("data/inpainting-tasks.json") as f:
        tasks = json.load(f)["tasks"]

    output_dir = os.path.join(args.output, args.workflow)
    os.makedirs(output_dir, exist_ok=True)

    workflow = load_workflow(args.workflow)
    workflow.run(tasks, output_dir)


if __name__ == "__main__":
    main()
