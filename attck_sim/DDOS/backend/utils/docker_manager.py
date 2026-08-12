import subprocess
import os
from pathlib import Path


# ------------------------------------------------------------
# Find project root (attack_sim folder)
# ------------------------------------------------------------
def get_project_root():
    """
    Returns absolute path of project root directory (attack_sim).
    Works regardless of where backend is executed.
    """
    current_file = Path(__file__).resolve()

    # backend/utils/docker_manager.py -> go up 3 levels
    project_root = current_file.parents[2]

    return project_root


def get_compose_file():
    """
    Return full path to docker-compose.yml inside DDOS folder
    """
    current = Path(__file__).resolve()

    # move up until attack_sim found
    for parent in current.parents:
        ddos_compose = parent / "DDOS" / "docker-compose.yml"
        if ddos_compose.exists():
            print("Using compose file:", ddos_compose)
            return str(ddos_compose)

    raise FileNotFoundError(
        "docker-compose.yml not found in attack_sim/DDOS"
    )


# ------------------------------------------------------------
# Start Lab
# ------------------------------------------------------------
def start_ddos_lab():
    """
    Starts all containers using docker-compose.
    """
    try:
        compose = get_compose_file()

        result = subprocess.run(
            ["docker-compose", "-f", compose, "up", "-d"],
            capture_output=True,
            text=True,
            check=True
        )

        return True, result.stdout

    except subprocess.CalledProcessError as e:
        return False, f"Docker error:\n{e.stderr}"

    except Exception as e:
        return False, str(e)


# ------------------------------------------------------------
# Stop Lab
# ------------------------------------------------------------
def stop_ddos_lab():
    """
    Stops and removes containers.
    """
    try:
        compose = get_compose_file()

        result = subprocess.run(
            ["docker-compose", "-f", compose, "down"],
            capture_output=True,
            text=True,
            check=True
        )

        return True, result.stdout

    except subprocess.CalledProcessError as e:
        return False, f"Docker error:\n{e.stderr}"

    except Exception as e:
        return False, str(e)


# ------------------------------------------------------------
# Check if Lab Running
# ------------------------------------------------------------
def lab_running():
    """
    Returns True if lab containers are running.
    """
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            text=True
        )

        # check for container names from docker-compose.yml
        containers = [
            "lab-target",
            "lab-simulator",
            "lab-detector"
        ]

        for c in containers:
            if c in result.stdout:
                return True

        return False

    except Exception:
        return False


# ------------------------------------------------------------
# Restart Lab
# ------------------------------------------------------------
def restart_lab():
    """
    Restart lab containers.
    """
    stop_ddos_lab()
    return start_ddos_lab()


# ------------------------------------------------------------
# Debug Helper
# ------------------------------------------------------------
def show_paths():
    """
    Prints detected project root and compose file.
    Useful for debugging.
    """
    try:
        root = get_project_root()
        compose = get_compose_file()

        return True, f"Root: {root}\nCompose: {compose}"

    except Exception as e:
        return False, str(e)
