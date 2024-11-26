import importlib


def load_workflow(workflow_name):
    try:
        workflow_module = importlib.import_module(f"workflows.{workflow_name}")
        return workflow_module
    except ModuleNotFoundError:
        raise ValueError(
            f"Workflow '{workflow_name}' not found in the 'workflows' package."
        )
