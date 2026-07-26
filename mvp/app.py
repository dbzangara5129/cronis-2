#!/usr/bin/env python3
"""
AI Task Automator MVP - Natural Language to Scheduled Tasks
Part of Project Cronis
"""

import json
import datetime
from pathlib import Path
import os

# LLM Integration (set API key via env)
try:
   from openai import OpenAI  # pip install openai
   LLM_AVAILABLE = True
except ImportError:
   LLM_AVAILABLE = False

DATA_DIR = Path(".chronis")
DATA_DIR.mkdir(exist_ok=True)
TASKS_FILE = DATA_DIR / "tasks.json"

def load_tasks():
   if TASKS_FILE.exists():
       return json.loads(TASKS_FILE.read_text())
   return {"tasks": []}

def save_tasks(tasks):
   TASKS_FILE.write_text(json.dumps(tasks, indent=2))

def parse_natural_to_cron(description):
   """
   LLM-powered natural language parser (fallback to rules).
   Set OPENAI_API_KEY env var for full AI parsing.
   """
   if LLM_AVAILABLE and os.getenv("OPENAI_API_KEY"):
       try:
           client = OpenAI()
           response = client.chat.completions.create(
               model="gpt-4o-mini",
               messages=[{
                   "role": "system",
                   "content": "You are a cron expert. Convert the description to a valid cron expression (5 fields) and a human-readable schedule. Return JSON: {'cron': '0 9 * * *', 'description': 'Daily at 9 AM'}"
               }, {
                   "role": "user",
                   "content": description
               }],
               temperature=0.1
           )
           result = json.loads(response.choices[0].message.content)
           return result["cron"], result["description"]
       except Exception as e:
           print(f"LLM fallback: {e}")

   # Enhanced rule-based fallback
   desc_lower = description.lower().strip()
   hour = 9
   if "at " in desc_lower:
       try:
           time_part = desc_lower.split("at ")[-1].split()[0]
           if ":" in time_part:
               hour = int(time_part.split(":")[0])
           else:
               hour = int(''.join(filter(str.isdigit, time_part)))
       except:
           pass

   if any(word in desc_lower for word in ["daily", "every day", "each day"]):
       return f"0 {hour} * * *", f"Daily at {hour}:00"
   elif any(word in desc_lower for word in ["monday", "mondays"]):
       return f"0 {hour} * * 1", f"Mondays at {hour}:00"
   elif any(word in desc_lower for word in ["weekly", "every week"]):
       return f"0 {hour} * * 1", f"Weekly at {hour}:00"
   elif "hour" in desc_lower:
       return "0 * * * *", "Every hour"
   elif "5 minutes" in desc_lower:
       return "*/5 * * * *", "Every 5 minutes"
   else:
       return f"0 {hour} * * *", f"Daily at {hour}:00 (fallback)"

def create_task(title, description=""):
   tasks = load_tasks()
   task_id = f"TASK-{len(tasks['tasks']) + 1:03d}"

   cron, schedule_desc = parse_natural_to_cron(description or title)

   task = {
       "id": task_id,
       "title": title,
       "description": description,
       "cron": cron,
       "schedule_desc": schedule_desc,
       "status": "open",
       "created": datetime.datetime.now().isoformat(),
       "events": [{"action": "created", "timestamp": datetime.datetime.now().isoformat()}]
   }

   tasks["tasks"].append(task)
   save_tasks(tasks)
   print(f"✅ Task created: {task_id} - {title}")
   print(f"   Schedule: {schedule_desc} ({cron})")
   return task_id

if __name__ == "__main__":
   import sys
   if len(sys.argv) > 1:
       title = " ".join(sys.argv[1:])
       create_task(title, title)
   else:
       print("Usage: python app.py 'Your task description here'")
