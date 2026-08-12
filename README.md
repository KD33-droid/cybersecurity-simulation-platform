# Cybersecurity Simulation Platform

A Docker-based cybersecurity simulation and teaching platform for demonstrating common security vulnerabilities and defensive concepts in isolated local lab environments.

The platform provides a central launcher and separate containerized labs for **DDoS simulation, SQL Injection, Cross-Site Scripting (XSS), and Authentication/Authorization weaknesses**. Each module is isolated through Docker Compose and can be started or stopped independently.

## Architecture

```text
                         Cyber Lab Launcher
                         FastAPI + Web UI
                                │
                  Docker Compose orchestration
                                │
        ┌───────────────┬───────┼────────┬───────────────┐
        ▼               ▼       ▼        ▼               
     DDoS Lab        SQLi Lab  XSS Lab  Auth Lab
        │               │       │        │
   Simulator +       Vulnerable/ Secure   Auth &
   Detector +       secure app  app       privilege
   Target + UI                             scenarios
        │               │       │        │
        └───────────────┴───────┴────────┘
                       Docker isolation
```

The launcher is a FastAPI application that starts and stops individual Docker Compose environments. The launcher container uses the Docker socket to orchestrate the local lab containers and mounts the project workspace into the container.

## Modules

### 1. DDoS Simulation Lab

The DDoS module is composed of separate services for:

- Traffic simulation
- Target application
- Detection engine
- Backend/orchestration
- Lab web UI

The module demonstrates how abnormal request traffic can affect an application and how a simple detection component can identify traffic above a configured threshold.

### 2. SQL Injection Lab

The SQL Injection module demonstrates the difference between an intentionally vulnerable authentication flow and a safer implementation using parameterized database queries.

The learning flow is:

```text
Vulnerable Application
        ↓
SQL Injection Demonstration
        ↓
Identify Root Cause
        ↓
Secure Implementation
        ↓
Parameterized Query
```

### 3. XSS Lab

The XSS module demonstrates client-side/script injection through intentionally vulnerable and safer rendering paths.

The module is designed to show:

- How unsanitized user-controlled content can become executable markup/script
- The difference between unsafe and safer output handling
- The importance of appropriate output encoding and input handling

### 4. Authentication Lab

The Authentication module demonstrates insecure authentication/authorization behavior and the security impact of trusting client-controlled parameters for privilege decisions.

The lab can be used to discuss:

- Authentication vs. authorization
- Broken access control
- Privilege escalation
- Server-side authorization checks

## Key Features

- Docker-based isolated cybersecurity labs
- Central FastAPI launcher
- Start/stop control for individual modules
- Dedicated Docker Compose environment per lab
- Vulnerable and safer application variants for selected web vulnerabilities
- DDoS traffic simulation and detection components
- Browser-based lab interfaces
- Local deployment without requiring cloud infrastructure

## Technology Stack

- Python
- FastAPI
- Flask
- Docker
- Docker Compose
- HTML/CSS/JavaScript
- SQLite
- REST-style HTTP endpoints

## Project Structure

```text
Cyberlab/
├── README.md
├── LICENSE
├── .gitignore
├── StartCyberlab.sh
├── screenshots/
│
└── attck_sim/
    ├── AUTH/
    │   ├── docker-compose.yml
    │   └── web/
    ├── DDOS/
    │   ├── backend/
    │   ├── detector/
    │   ├── simulator/
    │   ├── target/
    │   ├── ui/
    │   └── docker-compose.yml
    ├── Launcher/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── docker-compose.yml
    ├── SQLI/
    │   ├── docker-compose.yml
    │   └── web/
    ├── XSS/
    │   ├── docker-compose.yml
    │   └── web/
    └── start_cyberlab.sh
```

## Requirements

- Linux host recommended
- Docker
- Docker Compose
- Bash
- A browser

The platform is designed as a local cybersecurity lab and should not be exposed directly to an untrusted network.

## Running the Platform

From the project root:

```bash
chmod +x StartCyberlab.sh
./StartCyberlab.sh
```

The launcher starts on:

```text
http://localhost:5000
```

The launcher provides controls for starting and stopping the individual labs.

Alternatively, the launcher can be started from its directory:

```bash
cd attck_sim/Launcher
docker-compose up -d
```

## Lab Workflow

The platform is designed around a simple teaching workflow:

```text
Select Lab
    ↓
Start Isolated Environment
    ↓
Observe Vulnerable Behavior
    ↓
Demonstrate Attack
    ↓
Understand Detection / Impact
    ↓
Apply or Discuss Mitigation
    ↓
Stop Lab
```

This structure allows individual security concepts to be demonstrated without requiring the entire lab environment to run simultaneously.

## Security Considerations

> **This project intentionally contains vulnerable applications. Run it only in an isolated, authorized lab environment.**

The SQLi, XSS, authentication, and DDoS components are designed for controlled cybersecurity education and testing.

### Docker Socket Access

The launcher uses the host Docker socket so that it can orchestrate the individual lab Compose environments. This gives the launcher significant control over Docker on the host.

For that reason:

- Do not expose the launcher to an untrusted network.
- Do not deploy this configuration as a production service.
- Run the platform on a dedicated or disposable lab machine/VM where possible.
- Only allow authorized users to access the launcher.

### DDoS Module

The DDoS module is intended for controlled local simulation against the included lab target. Do not direct generated traffic toward systems or networks without explicit authorization.

## Educational Objectives

The platform is intended to provide hands-on demonstrations of:

- SQL Injection
- Cross-Site Scripting
- Authentication and authorization weaknesses
- Broken access control
- Privilege escalation concepts
- DDoS traffic generation and detection
- Container isolation
- Security monitoring and mitigation concepts

## Project Status

### Implemented

- Central FastAPI-based lab launcher
- Docker Compose orchestration
- SQL Injection lab
- XSS lab
- Authentication lab
- DDoS simulation environment
- DDoS detection component
- Browser-based lab interfaces
- Start/stop lifecycle management

### Future Improvements

Potential future improvements include:

- More vulnerability modules
- Improved detection and validation dashboards
- Automated mitigation demonstrations
- Better module status and health monitoring
- Structured learning paths for each vulnerability
- Additional API security scenarios
- Expanded documentation and lab exercises
- Automated environment cleanup

## Disclaimer

This project is an academic cybersecurity simulation platform. The vulnerable components are intentionally insecure and are provided solely for authorized educational and security-testing purposes.

Do not use the attack simulation components against systems or networks without explicit authorization.

## License

This project is released under the MIT License.

See [LICENSE](LICENSE) for details.
