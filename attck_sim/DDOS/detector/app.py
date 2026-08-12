from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Offline DDoS Detection Engine",
    version="1.0"
)

# -----------------------------
# Configuration
# -----------------------------
THRESHOLD_RPS = 10   # adjust after testing


# -----------------------------
# Detection Endpoint
# -----------------------------
@app.get("/status")
def check_status(rps: int = 0):
    timestamp = datetime.utcnow().isoformat()

    if rps > THRESHOLD_RPS:
        return {
            "timestamp": timestamp,
            "state": "ALERT",
            "action": "TAKE_SITE_DOWN",
            "observed_rps": rps,
            "threshold_rps": THRESHOLD_RPS,
            "reason": "Abnormal traffic volume detected (possible DDoS)"
        }

    return {
        "timestamp": timestamp,
        "state": "NORMAL",
        "action": "KEEP_SITE_UP",
        "observed_rps": rps,
        "threshold_rps": THRESHOLD_RPS,
        "reason": "Traffic within expected range"
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "service": "detector",
        "status": "UP",
        "threshold_rps": THRESHOLD_RPS
    }
