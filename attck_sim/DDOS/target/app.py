from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse
import time
import threading
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [TARGET] %(message)s"
)
logger = logging.getLogger("target")

app = FastAPI(title="Target Web Application")

REQUEST_COUNT = 0
CURRENT_STATE = "NORMAL"

DETECTOR_URL = "http://detector:9000/status"
RPS_INTERVAL = 1


# -----------------------------
# GLOBAL MIDDLEWARE (KEY FIX)
# -----------------------------
@app.middleware("http")
async def count_requests(request: Request, call_next):
    global REQUEST_COUNT

    REQUEST_COUNT += 1
    logger.info(f"Incoming request: {request.url.path} | Count={REQUEST_COUNT}")

    response = await call_next(request)
    return response


# -----------------------------
# Root Page
# -----------------------------
@app.get("/")
def homepage(response: Response):
    if CURRENT_STATE == "ALERT":
        response.status_code = 503
        return FileResponse("static/down.html")

    return FileResponse("static/index.html")


# -----------------------------
# Content API (ENFORCED)
# -----------------------------
@app.get("/content/{section}")
def load_content(section: str):
    if CURRENT_STATE == "ALERT":
        return JSONResponse(
            status_code=503,
            content={"error": "SERVICE_UNAVAILABLE"}
        )

    pages = {
        "home": "Welcome to Acme Corp.",
        "about": "We build secure, resilient systems.",
        "services": "Cloud Security, SOC Operations, DFIR.",
        "contact": "Email: support@acmecorp.local"
    }

    return {
        "title": section.capitalize(),
        "body": pages.get(section, "Page not found")
    }


# -----------------------------
# State API
# -----------------------------
@app.get("/state")
def state():
    return {"state": CURRENT_STATE}


# -----------------------------
# RPS Monitor
# -----------------------------
def monitor_rps():
    global REQUEST_COUNT, CURRENT_STATE
    logger.info("RPS monitor started")

    while True:
        time.sleep(RPS_INTERVAL)

        rps = REQUEST_COUNT
        REQUEST_COUNT = 0

        try:
            res = requests.get(
                DETECTOR_URL,
                params={"rps": rps},
                timeout=1
            )
            CURRENT_STATE = res.json().get("state", "NORMAL")
            logger.info(f"RPS={rps}, STATE={CURRENT_STATE}")
        except Exception as e:
            CURRENT_STATE = "NORMAL"
            logger.error(f"Detector error: {e}")


@app.on_event("startup")
def startup():
    threading.Thread(target=monitor_rps, daemon=True).start()
