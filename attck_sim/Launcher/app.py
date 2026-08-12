from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI(title="Cyber Lab Launcher")


# -----------------------------
# Helper function
# -----------------------------
import subprocess

def run_compose(module, action):
    path = f"/workspace/{module}/docker-compose.yml"

    cmd = ["docker-compose", "-f", path, action]

    if action == "up":
        cmd.append("-d")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        return {
            "cmd": " ".join(cmd),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# UI
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <head>
        <title>Cyber Lab Launcher</title>

        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #f1f5f9;
                color: #1e293b;
                padding: 40px;
            }

            .container {
                max-width: 900px;
                margin: auto;
            }

            /* 🔥 Gradient Title */
            .title {
                text-align: center;
                margin-bottom: 30px;
                font-size: 32px;
                font-weight: 700;
                background: linear-gradient(90deg, #2563eb, #06b6d4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            /* 🔥 Module Card */
            .module {
                background: #ffffff;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;

                /* added effects */
                border-top: 4px solid #2563eb;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            .module:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 18px rgba(0,0,0,0.12);
            }

            .module h3 {
                margin-bottom: 10px;
            }

            .status {
                font-size: 14px;
                margin-bottom: 10px;
            }

            .running { color: #16a34a; }
            .stopped { color: #dc2626; }
            .loading { color: #d97706; }

            button {
                padding: 10px 15px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                margin-right: 10px;
                font-weight: bold;
            }

            .start {
                background: #22c55e;
                color: white;
            }

            .stop {
                background: #ef4444;
                color: white;
            }

            button:hover {
                opacity: 0.9;
            }
        </style>
    </head>

    <body>

        <div class="container">
            <h1 class="title">Cyber Lab Launcher</h1>

            <div class="module">
                <h3>DDoS Lab</h3>
                <div class="status stopped" id="status-DDOS">● Stopped</div>
                <button class="start" onclick="start('DDOS')">Start</button>
                <button class="stop" onclick="stop('DDOS')">Stop</button>
            </div>

            <div class="module">
                <h3>SQL Injection Lab</h3>
                <div class="status stopped" id="status-SQLI">● Stopped</div>
                <button class="start" onclick="start('SQLI')">Start</button>
                <button class="stop" onclick="stop('SQLI')">Stop</button>
            </div>

            <div class="module">
                <h3>XSS Lab</h3>
                <div class="status stopped" id="status-XSS">● Stopped</div>
                <button class="start" onclick="start('XSS')">Start</button>
                <button class="stop" onclick="stop('XSS')">Stop</button>
            </div>

            <div class="module">
                <h3>Authentication Lab</h3>
                <div class="status stopped" id="status-AUTH">● Stopped</div>
                <button class="start" onclick="start('AUTH')">Start</button>
                <button class="stop" onclick="stop('AUTH')">Stop</button>
            </div>
        </div>

        <script>
            function updateStatus(module, state) {
                const el = document.getElementById("status-" + module);

                el.className = "status " + state;

                if (state === "running") el.innerHTML = "● Running";
                if (state === "stopped") el.innerHTML = "● Stopped";
                if (state === "loading") el.innerHTML = "● Working...";
            }

            async function start(module) {
                updateStatus(module, "loading");

                await fetch(`/start/${module}`);

                updateStatus(module, "running");

                setTimeout(() => {
                    window.location.href = `/lab/${module}`;
                }, 2000);
            }

            async function stop(module) {
                updateStatus(module, "loading");

                await fetch(`/stop/${module}`);

                updateStatus(module, "stopped");
            }
            async function loadStatus() {
                const res = await fetch("/status");
                const data = await res.json();

                for (let module in data) {
                    if (data[module]) {
                        updateStatus(module, "running");
                    } else {
                        updateStatus(module, "stopped");
                    }
                }
            }     
            loadStatus();
        </script>

    </body>
    </html>
    """
# -----------------------------
# API endpoints
# -----------------------------
@app.get("/start/{module}")
def start_module(module: str):
    return run_compose(module, "up")


@app.get("/stop/{module}")
def stop_module(module: str):
    return run_compose(module, "down")

@app.get("/status")
def get_status():
    result = subprocess.check_output(["docker", "ps"]).decode()

    return {
        "DDOS": "lab-target" in result,
        "SQLI": "sqli-web" in result,
        "XSS": "xss-web" in result,
        "AUTH": "auth-web" in result
    }
    
# -----------------------------
# Lab Info (STATIC MAPPING - BEST FOR DEMO)
# -----------------------------
@app.get("/lab-info/{module}")
def lab_info(module: str):
    module = module.upper()

    data = {
        "DDOS": {
            "Target Server": "http://localhost:8080",
            "Traffic Simulator": "http://localhost:4000"
        },
        "SQLI": {
            "Vulnerable App": "http://localhost:5050"
        },
        "XSS": {
            "Comment App": "http://localhost:7070"
        },
        "AUTH": {
            "Login App": "http://localhost:6060"
        }
    }

    return data.get(module, {"error": "Unknown module"})    




@app.get("/lab/{module}", response_class=HTMLResponse)
def lab_page(module: str):
    return f"""
    <html>
    <head>
        <title>{module} Lab</title>

        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #f1f5f9;
                color: #1e293b;
                padding: 40px;
            }}

            .container {{
                max-width: 800px;
                margin: auto;
            }}

            .title {{
                text-align: center;
                margin-bottom: 30px;
                font-size: 30px;
                font-weight: 700;
                background: linear-gradient(90deg, #2563eb, #06b6d4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .card {{
                background: #ffffff;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
                border-top: 4px solid #2563eb;
            }}

            .link-block {{
                margin-top: 15px;
                padding: 10px;
                background: #f8fafc;
                border-radius: 6px;
                border: 1px solid #e2e8f0;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            .link-block:hover {{
                  transform: translateY(-2px);
                  box-shadow: 0 6px 14px rgba(0,0,0,0.08);
            }}
            a {{
                color: #2563eb;
                text-decoration: none;
                font-weight: 500;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            .back {{
                display: inline-block;
                margin-bottom: 20px;
                color: #64748b;
                text-decoration: none;
                font-size: 14px;
            }}

            .back:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <a href="/" class="back">← Back to Dashboard</a>

            <h1 class="title">{module} Lab Running</h1>

            <div class="card">
                <div id="links"></div>
            </div>

        </div>

        <script>
            async function loadLinks() {{
                const res = await fetch("/lab-info/{module}");
                const data = await res.json();

                let html = "";

                for (let key in data) {{
                    html += `
                        <div class="link-block">
                            <strong>${{key}}</strong><br>
                            <a href="${{data[key]}}" target="_blank">${{data[key]}}</a>
                        </div>
                    `;
                }}

                document.getElementById("links").innerHTML = html;
            }}

            loadLinks();
        </script>

    </body>
    </html>
    """
