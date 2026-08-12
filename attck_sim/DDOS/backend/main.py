from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.docker_manager import (
    start_ddos_lab,
    stop_ddos_lab,
    lab_running
)

app = FastAPI()

# allow UI access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/start-ddos")
def start_ddos():
    ok, msg = start_ddos_lab()
    return {"success": ok, "message": msg}

@app.post("/stop-ddos")
def stop_ddos():
    ok, msg = stop_ddos_lab()
    return {"success": ok, "message": msg}

@app.get("/lab-status")
def status():
    return {"running": lab_running()}
