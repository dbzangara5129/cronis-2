from flask import Flask, request
import datetime

app = Flask(__name__)
tasks = []

@app.route("/", methods=["GET", "POST"]) def home():
    message = ""
    if request.method == "POST":
        title = request.form.get("task", "").strip()
        if title:
            schedule = "Daily at 9:00"
            if "monday" in title.lower():
                schedule = "Mondays at 9:00"
            tasks.append({"title": title, "schedule": schedule})
            message = "Task added!"
        else:
            message = "Please type a task."

    html = "<html><body style='font-family:sans-serif;max-width:600px;margin:40px auto;padding:20px'>"
    html += "<h1>Cronis AI</h1>"
    html += "<p>Enter a task in natural language</p>"
    html += "<form method='POST'>"
    html += "<input name='task' style='width:100%;padding:10px' placeholder='e.g. every Monday at 9am' required>"
    html += "<br><br><button type='submit' style='padding:10px 20px;background:#667eea;color:white;border:none'>Create Task</button>"
    html += "</form>"
    html += f"<p style='color:green'>{message}</p>"
    html += "<h2>Tasks</h2>"

    if tasks:
        for t in tasks:
            html += f"<div style='background:#f1f5f9;padding:10px;margin:8px 0'><b>{t['title']}</b><br>{t['schedule']}</div>"
    else:
        html += "<p>No tasks yet.</p>"

    html += "</body></html>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


