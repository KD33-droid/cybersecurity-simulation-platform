from flask import Flask, request, redirect

app = Flask(__name__)

# ---------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        # ❌ BROKEN AUTH (no password validation)
        if username == "admin":
            return redirect("/dashboard?role=admin")
        else:
            return redirect("/dashboard?role=user")

    return """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Login</title>
    <style>
    body {
        background:#0f172a;
        font-family:Arial;
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }
    .card {
        background:#1e293b;
        padding:30px;
        border-radius:10px;
        width:300px;
        box-shadow:0 0 20px rgba(0,0,0,0.5);
    }
    input {
        width:100%;
        padding:10px;
        margin:10px 0;
        border-radius:5px;
        border:none;
    }
    button {
        width:100%;
        padding:10px;
        background:#3b82f6;
        color:white;
        border:none;
        border-radius:5px;
        cursor:pointer;
    }
    button:hover {
        background:#2563eb;
    }
    </style>
    </head>

    <body>
    <div class="card">
        <h2>🔐 Secure Portal</h2>

        <form method="POST">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>

        <p style="font-size:12px;color:#94a3b8;">
        Hint: Try logging in as a normal user
        </p>
    </div>
    </body>
    </html>
    """


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
@app.route("/dashboard")
def dashboard():
    role = request.args.get("role")

    if role == "admin":
        return admin_panel()

    return """
    <html>
    <head>
    <style>
    body {
        background:#0f172a;
        color:white;
        font-family:Arial;
        padding:30px;
    }
    .card {
        background:#1e293b;
        padding:20px;
        border-radius:10px;
        margin:15px 0;
    }
    </style>
    </head>

    <body>

    <h1>User Dashboard</h1>

    <div class="card">
        <p>Welcome user 👋</p>
        <p>You have limited access.</p>
    </div>

    <div class="card">
        <h3>Try this:</h3>
        <p>Modify the URL:</p>
        <pre>?role=admin</pre>
    </div>

    </body>
    </html>
    """


# ---------------------------------------------------
# ADMIN PANEL (IMPACT)
# ---------------------------------------------------
def admin_panel():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        background:#0f172a;
        color:white;
        font-family:Arial;
        padding:30px;
    }
    .header {
        font-size:24px;
        margin-bottom:20px;
    }
    .card {
        background:#1e293b;
        padding:20px;
        border-radius:10px;
        margin:15px 0;
    }
    .alert {
        color:#f87171;
        font-weight:bold;
    }
    </style>
    </head>

    <body>

    <div class="header">🔐 Admin Panel</div>

    <div class="card">
        <h3>👤 Admin Access Granted</h3>
        <p>You now have full system control.</p>
    </div>

    <div class="card">
        <h3>📂 User Credentials</h3>
        <ul>
            <li>admin / admin123</li>
            <li>student / password123</li>
        </ul>
    </div>

    <div class="card">
        <h3>💳 Sensitive Data</h3>
        <ul>
            <li>Credit Card: 4111-1111-1111</li>
            <li>API Key: SECRET-ADMIN-KEY</li>
        </ul>
    </div>

    <div class="card alert">
        ⚠️ Privilege Escalation via Broken Authentication!
    </div>

    <a href="/" style="color:#3b82f6;">Logout</a>

    </body>
    </html>
    """


# ---------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
