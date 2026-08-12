from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_FILE = "users.db"

# -------------------------------
# HTML UI
# -------------------------------
page = """
<!DOCTYPE html>
<html>
<head>
<title>SQL Injection Lab</title>

<style>
body {
    font-family: Arial;
    background: #0f172a;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    background: #1e293b;
    padding: 30px;
    border-radius: 10px;
    width: 350px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
}

h2 {
    text-align: center;
}

input {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border-radius: 5px;
    border: none;
}

button {
    width: 100%;
    padding: 10px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background: #2563eb;
}

.msg {
    margin-top: 10px;
    text-align: center;
}

.query {
    margin-top: 15px;
    background: #020617;
    padding: 10px;
    font-size: 12px;
    border-radius: 5px;
}

.tip {
    margin-top: 15px;
    font-size: 13px;
    color: #94a3b8;
}
</style>
</head>

<body>

<div class="container">
<h2>🔐 SQL Injection Lab</h2>

<form method="POST">
<input name="username" placeholder="Username">
<input name="password" placeholder="Password" type="password">
<button type="submit">Login</button>
</form>

<div class="msg">{{msg}}</div>

{% if query %}
<div class="query">
<b>Executed Query:</b><br>
{{query}}
</div>
{% endif %}

<div class="tip">
Try: <code>admin' -- </code>
</div>

</div>

</body>
</html>
"""

# -------------------------------
# Vulnerable Login
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    query = ""

    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        query = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"

        try:
            result = c.execute(query).fetchone()

            if result:
                return redirect(url_for("admin"))   # 🔥 REDIRECT HERE
            else:
                msg = "❌ Invalid Login"

        except Exception as e:
            msg = f"SQL Error: {e}"

        conn.close()

    return render_template_string(page, msg=msg, query=query)

#
# Admin Page
# -------------------------------

@app.route("/admin")
def admin():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Admin Dashboard</title>

    <style>
    body {
        font-family: Arial;
        background: #0f172a;
        color: white;
        padding: 30px;
    }

    .header {
        font-size: 24px;
        margin-bottom: 20px;
    }

    .card {
        background: #1e293b;
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
    }

    .alert {
        color: #f87171;
        font-weight: bold;
    }
    </style>
    </head>

    <body>

    <div class="header">🔐 Admin Dashboard</div>

    <div class="card">
        <h3>👤 Logged in as Admin</h3>
        <p>You now have full system access.</p>
    </div>

    <div class="card">
        <h3>📂 User Data</h3>
        <ul>
            <li>admin / admin123</li>
            <li>student / password123</li>
            <li>guest / guest123</li>
        </ul>
    </div>

    <div class="card">
        <h3>💳 Sensitive Information</h3>
        <ul>
            <li>Credit Card: 4111-1111-1111-1111</li>
            <li>API Key: SECRET-KEY-123</li>
        </ul>
    </div>

    <div class="card alert">
        ⚠️ Access obtained via SQL Injection!
    </div>

    <a href="/" style="color:#3b82f6;">Logout</a>

    </body>
    </html>
    """
# -------------------------------
# Secure Version
# -------------------------------
@app.route("/secure", methods=["GET", "POST"])
def secure():
    msg = ""

    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # ✅ Safe query
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        )

        result = c.fetchone()

        if result:
            msg = "Login Success (Secure)"
        else:
            msg = "Invalid Login"

        conn.close()

    return render_template_string(page, msg=msg, query="Prepared Statement Used")


# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
