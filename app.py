from flask import Flask, request, render_template_string import datetime import traceback

app = Flask(__name__)
tasks = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Cronis AI</title>
    <style>
        body { font-family: system-ui; max-width: 700px; margin: 40px auto; padding: 20px; }
        input, button { padding: 12px; font-size: 16px; margin: 8px 0; width: 100%; box-sizing: border-box; }
        button { background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; }
        .task { background: #f1f5f9; padding: 12px; margin: 10px 0; border-radius: 8px; }
        .error { background: #fee2e2; color: #b91c1c; padding: 12px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Cronis AI – Task Automator</h1>
    <p>Type a task in natural language (example: every Monday at 9am generate report)</p>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}
    
    <form method="POST">
        <input type="text" name="task" placeholder="Describe your task..." required>
        <button type="submit">Create Task</button>
    </form>

    <h2>Your Tasks</h2>
    {% for t in tasks %}
        <div class="task">
            <strong>{{ t.title }}</strong><br>
            Schedule: {{ t.schedule }}
        </div>
    {% else %}
        <p>No tasks yet.</p>
    {% endfor %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"]) def home():
    error = None
    try:
        if request.method == "POST":
            title = request.form.get("task", "").strip()
            if not title:
                error = "Please enter a task description."
