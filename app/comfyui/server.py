import os
import re
import socket
import subprocess
import tempfile
import time

import psutil


COMFYUI_PIP_DEPENDENCIES = [
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
    ["gguf"],
]


def _install_cloudflared():
    try:
        result = subprocess.run(
            ["cloudflared", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            print("Cloudflared is already installed.")
            return
    except FileNotFoundError:
        print("Cloudflared is not installed. Installing...")

    try:
        subprocess.run(
            [
                "wget",
                "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb",  # noqa: E501
            ],
            check=True,
        )
        subprocess.run(["dpkg", "-i", "cloudflared-linux-amd64.deb"], check=True)
        print("Cloudflared installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during cloudflared installation: {e}")
        raise


def _install_comfyui_pip_dependencies():
    print("Installing ComfyUI pip dependencies\n")
    for dependency in COMFYUI_PIP_DEPENDENCIES:
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


def _is_server_running(host: str = "127.0.0.1", port: int = 8188) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((host, port))
        if result == 0:
            return True

    return False


def _start_comfyui_server():
    assert os.environ.get(
        "COMFYUI_INSTALL_DIR"
    ), "Missing environment variable COMFYUI_INSTALL_DIR"

    if _is_server_running():
        print("ComfyUI server is already running.")
        return

    stdout_file = tempfile.NamedTemporaryFile(
        delete=False, mode="w+", suffix=".log", prefix="comfyui_stdout_"
    )
    stderr_file = tempfile.NamedTemporaryFile(
        delete=False, mode="w+", suffix=".log", prefix="comfyui_stderr_"
    )

    try:
        process = subprocess.Popen(
            [
                "python",
                os.path.join(os.environ["COMFYUI_INSTALL_DIR"], "main.py"),
            ],
            stdout=stdout_file,
            stderr=stderr_file,
        )
        print(f"\n\nComfyUI server started with PID {process.pid}")
        print(f"stdout redirected to: {stdout_file.name}")
        print(f"stderr redirected to: {stderr_file.name}\n\n")

        with open(stdout_file.name, "r") as stdout_reader, open(
            stderr_file.name, "r"
        ) as stderr_reader:
            stdout_reader.seek(0, os.SEEK_END)  # Start reading from the end of the file
            stderr_reader.seek(0, os.SEEK_END)

            while True:
                stdout_line = stdout_reader.readline()
                stderr_line = stderr_reader.readline()
                if stdout_line:
                    print(f"[stdout]: {stdout_line.strip()}")
                if stderr_line:
                    print(f"[stderr]: {stderr_line.strip()}")

                    if "To see the GUI go to: http://127.0.0.1:8188" in stderr_line:
                        print("GUI URL detected. Server is ready.")
                        break

                if process.poll() is not None:
                    raise RuntimeError("ComfyUI server process exited unexpectedly.")

                time.sleep(1)

    except Exception as e:
        print(f"Failed to start ComfyUI server: {e}")
        print(f"Failed to start ComfyUI server: {e}")
        print(
            f"Attempting to print and delete logs from:\nstdout: {stdout_file.name}\
            \nstderr: {stderr_file.name}\n"
        )
        _print_and_cleanup_logs(stdout_file.name, stderr_file.name)
        raise

    return


def _start_cloudflared_tunnel(host: str, port: int, timeout=180):
    if not _is_server_running(host, port):
        raise RuntimeError(f"Server is not running on http://{host}:{port}")

    try:
        p = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://{host}:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print(f"Timeout reached ({timeout}s). Cloudflared failed to start.")
                p.terminate()
                p.wait()
                return

            if p and p.stderr:
                for line in iter(p.stderr.readline, ""):
                    if "trycloudflare.com" in line:
                        tunnel_url = line[line.find("http") :].strip()
                        match = re.match(
                            r"https:\/\/[a-z0-9-]+\.trycloudflare\.com", tunnel_url
                        )
                        if match:
                            print(f"\n\nYou can access ComfyUI at: {tunnel_url}\n\n")
                            return

            time.sleep(1)

    except Exception as e:
        print(f"Error while launching Cloudflare tunnel: {e}")
        p.terminate() if p else None


def start(skip_dep_installation: bool = False):
    if not skip_dep_installation:
        _install_comfyui_pip_dependencies()
        _install_cloudflared()

    _start_comfyui_server()
    _start_cloudflared_tunnel(host="127.0.0.1", port=8188)


def stop():
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        if "cloudflared" in p.info["name"]:
            print(f"Terminating {p.info['name']} with PID {p.info['pid']}")
            try:
                p.terminate()
            except Exception as e:
                print(f"Failed to delete Cloudflared tunnel process, {e}")

        if "comfyui" in "".join(p.info["cmdline"]).lower():
            print(f"Terminating {p.info['name']} with PID {p.info['pid']}")
            try:
                p.terminate()
            except Exception as e:
                print(f"Failed to delete ComfyUI server process, {e}")
