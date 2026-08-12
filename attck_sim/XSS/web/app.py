from flask import Flask, request, render_template_string

app = Flask(__name__)

comments = []

# ---------------------------------------------------
# MAIN PAGE (VULNERABLE)
# ---------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    global comments

    if request.method == "POST":
        comment = request.form["comment"]

        # ❌ VULNERABLE (no sanitization)
        comments.append(comment)

    page = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>XSS Lab</title>

    <style>
    body {
        font-family: Arial;
        background: #0f172a;
        color: white;
        padding: 30px;
    }

    .container {
        max-width: 600px;
        margin: auto;
    }

    .card {
        background: #1e293b;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    input, button {
        padding: 10px;
        width: 100%;
        margin-top: 10px;
        border-radius: 5px;
        border: none;
    }

    button {
        background: #3b82f6;
        color: white;
        cursor: pointer;
    }

    button:hover {
        background: #2563eb;
    }

    .comment {
        background: #020617;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }

    .hint {
        color: #94a3b8;
        font-size: 14px;
    }
    </style>
    </head>

    <body>

    <div class="container">

        <h1>💬 Comment Portal</h1>

        <div class="card">
            <form method="POST">
                <input name="comment" placeholder="Enter your comment">
                <button type="submit">Post Comment</button>
            </form>

            <p class="hint">
            Try injecting: &lt;script&gt;alert('XSS')&lt;/script&gt;
            </p>
        </div>

        <div class="card">
            <h3>💭 Comments</h3>
            {% for c in comments %}
                <div class="comment">{{c|safe}}</div>
            {% endfor %}
        </div>

    </div>

    </body>
    </html>
    """

    return render_template_string(page, comments=comments)


# ---------------------------------------------------
# SECURE VERSION
# ---------------------------------------------------
@app.route("/secure", methods=["GET", "POST"])
def secure():
    safe_comments = []

    if request.method == "POST":
        comment = request.form["comment"]
        safe_comments.append(comment)

    page = """
    <h2>Secure Comment Page</h2>

    <form method="POST">
        <input name="comment">
        <button type="submit">Post</button>
    </form>

    <h3>Comments:</h3>
    {% for c in comments %}
        <p>{{c}}</p>
    {% endfor %}
    """

    return render_template_string(page, comments=safe_comments)


# ---------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
