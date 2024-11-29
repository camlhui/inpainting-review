import os
import subprocess
import tempfile


PIP_DEPENDENCIES = dependencies = [
    ["accelerate"],
    ["einops"],
    ["transformers>=4.28.1"],
    ["safetensors>=0.4.2"],
    ["aiohttp"],
    ["pyyaml"],
    ["Pillow"],
    ["scipy"],
    ["tqdm"],
    ["psutil"],
    ["tokenizers>=0.13.3"],
    [
        "torch",
        "torchvision",
        "torchaudio",
        "--index-url",
        "https://download.pytorch.org/whl/cu121",
    ],
    ["torchsde"],
    ["kornia>=0.7.1"],
    ["spandrel"],
    ["soundfile"],
    ["sentencepiece"],
]


def _install_pip_dependencies():
    print("Installing pip dependencies")
    for dependency in dependencies:
        try:
            print(f"Installing: {' '.join(dependency)}")
            result = subprocess.run(
                ["pip3", "install"] + dependency,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode != 0:
                print(f"Failed to install {' '.join(dependency)}: {result.stderr}")
                raise subprocess.CalledProcessError(
                    result.returncode,
                    result.args,
                    output=result.stdout,
                    stderr=result.stderr,
                )
            else:
                print(f"Successfully installed {' '.join(dependency)}")
        except subprocess.CalledProcessError as e:
            print(f"Error while installing {' '.join(dependency)}:\n{e.stderr}")
            raise


def _print_and_cleanup_logs(stdout_file: str, stderr_file: str):
    print("\n--- stdout ---")
    with open(stdout_file, "r") as f:
        print(f.read())

    print("\n--- stderr ---")
    with open(stderr_file, "r") as f:
        print(f.read())

    os.remove(stdout_file)
    os.remove(stderr_file)
    print("\nTemporary log files have been deleted.")


def start_comfyui_server():
    _install_pip_dependencies()

    stdout_file = tempfile.NamedTemporaryFile(
        delete=False, mode="w+", suffix=".log", prefix="comfyui_stdout_"
    )
    stderr_file = tempfile.NamedTemporaryFile(
        delete=False, mode="w+", suffix=".log", prefix="comfyui_stderr_"
    )

    assert os.environ.get(
        ["COMFYUI_INSTALL_DIR"]
    ), "Missing environment variable COMFYUI_INSTALL_DIR"

    try:
        process = subprocess.Popen(
            [
                "python",
                os.path.join(os.environ.get(["COMFYUI_INSTALL_DIR"]), "main.py"),
            ],
            stdout=stdout_file,
            stderr=stderr_file,
        )

        print(f"ComfyUI server started with PID {process.pid}")
        print(f"stdout redirected to: {stdout_file.name}")
        print(f"stderr redirected to: {stderr_file.name}")

        return process, stdout_file.name, stderr_file.name

    except Exception as e:
        print(f"Failed to start ComfyUI server: {e}")
        print(f"Failed to start ComfyUI server: {e}")
        print(
            f"Attempting to print and delete logs from:\nstdout: {stdout_file.name}\
            \nstderr: {stderr_file.name}\n"
        )
        _print_and_cleanup_logs(stdout_file.name, stderr_file.name)
        raise


def stop_comfyui_server(process: subprocess.Popen, stdout_file: str, stderr_file: str):
    if process and process.poll() is None:
        print("Stopping the server...")
        process.terminate()
        process.wait()
        print("Server stopped.")

        print(
            f"Attempting to print and delete logs from:\nstdout: {stdout_file}\
            \nstderr: {stderr_file}\n"
        )
        _print_and_cleanup_logs(stdout_file, stderr_file)
    else:
        print("Server is not running or already stopped.")
