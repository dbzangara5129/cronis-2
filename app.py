from flask import Flask, request, render_template_string import datetime

app = Flask(__name__)
tasks = []

@app.route("/", methods=["GET", "POST"]) def home():
    error = ""
    if request.method == "POST":
        title = request.form.get("task", "").strip()
        if title:
            schedule = "Daily at 9:00"
            if "monday" in title.lower():
                schedule = "Mondays at 9:00"
            tasks.append({"title": title, "schedule": schedule})
        else:
            error = "Please enter a task."

    html = f"""
    <html>
    <head><title>Cronis AI</title></

