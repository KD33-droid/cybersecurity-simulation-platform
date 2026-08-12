from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading
import requests
import time
import os
import logging

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [SIMULATOR] %(message)s"
)
logger = logging.getLogger("simulator")

app = FastAPI(title="Attack Simulator Dashboard")

# -----------------------------
# Configuration
# -----------------------------
TARGET_URL = os.getenv("TARGET_URL", "http://target")
MODE = "STOP"
THREAD = None


# -----------------------------
# Traffic Generator
# -----------------------------
def traffic_generator():
    global MODE
    logger.info("Traffic generator started")

    while MODE != "STOP":
        try:
            requests.get(TARGET_URL, timeout=0.5)
        except Exception as e:
            logger.error(f"Request error: {e}")

        if MODE == "NORMAL":
            time.sleep(0.3)      # ~3 RPS
        elif MODE == "ATTACK":
            time.sleep(0.005)    # ~200 RPS


# -----------------------------
# Dashboard UI
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Attack Simulator Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
        }
        header {
            background: #1f2933;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        .status {
            font-size: 20px;
            margin-bottom: 20px;
        }
        .badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            color: white;
        }
        .STOP { background: #6b7280; }
        .NORMAL { background: #16a34a; }
        .ATTACK { background: #dc2626; }

        .buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
        }
        button {
            flex: 1;
            margin: 0 10px;
            padding: 15px;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            color: white;
        }
        .normal-btn { background: #16a34a; }
        .attack-btn { background: #dc2626; }
        .stop-btn { background: #374151; }

        button:hover {
            opacity: 0.85;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            color: #6b7280;
            font-size: 14px;
        }
    </style>
</head>

<body>
    <header>
        <h1>🧪 Attack Simulation Control Panel</h1>
        <p>Offline Cybersecurity Attack Lab</p>
    </header>

    <div class="container">
        <div class="status">
            Current Status:
            <span id="statusBadge" class="badge STOP">STOPPED</span>
        </div>

        <div class="buttons">
            <button class="normal-btn" onclick="start('normal')">
                ▶ Start Normal Traffic
            </button>
            <button class="attack-btn" onclick="start('attack')">
                ⚠ Start Attack
            </button>
            <button class="stop-btn" onclick="stopAttack()">
                ⏹ Stop
            </button>
        </div>
    </div>

    <footer>
        <p>Offline Attack Simulation & Detection Framework</p>
    </footer>

<script>
    async function refreshStatus() {
        const res = await fetch('/status');
        const data = await res.json();
        const badge = document.getElementById('statusBadge');

        badge.textContent = data.mode;
        badge.className = 'badge ' + data.mode;
    }

    async function start(mode) {
        await fetch('/start/' + mode);
        refreshStatus();
    }

    async function stopAttack() {
        await fetch('/stop');
        refreshStatus();
    }

    setInterval(refreshStatus, 1000);
</script>
</body>
</html>
"""


# -----------------------------
# Control APIs
# -----------------------------
@app.get("/start/{mode}")
def start(mode: str):
    global MODE, THREAD

    mode = mode.upper()
    if mode not in ["NORMAL", "ATTACK"]:
        return {"error": "Invalid mode"}

    MODE = mode
    logger.info(f"Mode set to {MODE}")

    if THREAD is None or not THREAD.is_alive():
        THREAD = threading.Thread(target=traffic_generator, daemon=True)
        THREAD.start()

    return {"mode": MODE}


@app.get("/stop")
def stop():
    global MODE
    MODE = "STOP"
    logger.info("Traffic stopped")
    return {"mode": MODE}


@app.get("/status")
def status():
    return {"mode": MODE}

