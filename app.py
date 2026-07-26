from flask import Flask, request, render_template_string import datetime import json from pathlib import Path

app = Flask(__name__)

# Simple in-memory storage for demo
tasks = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cronis AI</title>
    <style>
        body { font-family: system-ui; max-width: 700px; margin: 40px auto; padding: 20px; }
        input, button { padding: 12px; font-size: 16px; margin: 8px 0; width: 100%; }
        button { background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; }
        .task { background: #f1f5f9; padding: 12px; margin: 10px 0; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Cronis AI – Task Automator</h1>
    <p>Type a task in natural language (e.g. "every Monday at 9am generate report")</p>
    
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
    {% endfor %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"]) def home():
    if request.method == "POST":
        title = request.form.get("task")
        # Simple schedule detection (same logic as before)
        schedule = "Daily at 9:00 (demo)"
        if "monday" in title.lower():
            schedule = "Mondays at 9:00"
        tasks.append({
            "title": title,
            "schedule": schedule,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    return render_template_string(HTML, tasks=tasks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
