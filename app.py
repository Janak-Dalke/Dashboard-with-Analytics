from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import requests as http_req
import os
from dotenv import load_dotenv

load_dotenv()  # loads from .env file automatically

app = Flask(__name__, static_folder=".")
CORS(app)

# Key is loaded from .env file — never hardcoded
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

USERS_MONTHLY = {
    "labels": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    "data":   [120,190,170,240,310,280,350,420,390,460,510,580]
}
TASKS_BY_CATEGORY = {
    "labels": ["Development","Design","Marketing","Support","Research"],
    "data":   [340,210,180,290,150]
}
REVENUE_WEEKLY = {
    "labels": ["Week 1","Week 2","Week 3","Week 4"],
    "data":   [12400,18700,15300,22100]
}
PERFORMANCE = {
    "labels":    ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    "completed": [45,62,58,71,83,39,27],
    "pending":   [12,8,15,9,6,18,21]
}

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/stats")
def get_stats():
    return jsonify({"total_users":5820,"tasks_completed":3194,"revenue":68500,
                    "active_projects":24,"user_growth":"+12.4%","task_growth":"+8.7%",
                    "revenue_growth":"+19.2%","project_growth":"+4"})

@app.route("/api/users/monthly")
def get_users_monthly():
    return jsonify(USERS_MONTHLY)

@app.route("/api/tasks/category")
def get_tasks_by_category():
    return jsonify(TASKS_BY_CATEGORY)

@app.route("/api/revenue/weekly")
def get_revenue_weekly():
    return jsonify(REVENUE_WEEKLY)

@app.route("/api/performance/weekly")
def get_performance():
    return jsonify(PERFORMANCE)


@app.route("/api/analyze", methods=["POST"])
def analyze_dataset():
    body     = request.get_json(force=True)
    dataset  = body.get("dataset", "").strip()
    filename = body.get("filename", "dataset")

    if not GROQ_API_KEY:
        return jsonify({"error": "GROQ_API_KEY not found. Please add it to your .env file."}), 400
    if not dataset:
        return jsonify({"error": "Dataset is empty."}), 400

    truncated = dataset[:10000]

    prompt = f"""You are a senior data analyst. Analyze this dataset and respond ONLY with valid JSON.
No markdown, no backticks, no explanation — just raw JSON.

Dataset filename: {filename}
Dataset:
{truncated}

Return exactly this JSON structure:
{{
  "summary": "2-3 sentence executive summary",
  "insights": ["insight 1", "insight 2", "insight 3", "insight 4"],
  "kpis": [
    {{"label": "KPI Name", "value": "formatted value", "trend": "+X% or -X% or neutral"}}
  ],
  "charts": [
    {{
      "title": "Chart Title",
      "subtitle": "What this shows",
      "type": "line or bar or doughnut or radar",
      "labels": ["label1", "label2"],
      "datasets": [
        {{"label": "Series Name", "data": [1, 2, 3]}}
      ],
      "insight": "One sentence chart insight"
    }}
  ]
}}

Rules:
- 3 to 5 charts using best chart types for the data
- All numbers must be real values from the dataset
- 3 to 4 KPIs, exactly 4 insights
- Labels max 15 chars
- Return ONLY raw JSON, nothing else"""

    try:
        resp = http_req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 2048
            },
            timeout=60
        )

        if resp.status_code != 200:
            msg = resp.json().get("error", {}).get("message", resp.text[:200])
            return jsonify({"error": f"Groq error: {msg}"}), 500

        raw = resp.json()["choices"][0]["message"]["content"].strip()

        if "```" in raw:
            parts = raw.split("```")
            raw = parts[1] if len(parts) > 1 else raw
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        print(f"Analysis done: {filename}")
        return jsonify(result)

    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON from Groq: {str(e)} | {raw[:150]}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\U0001f680  Analytics API \u2192 http://127.0.0.1:5000")
    print(f"  Groq key loaded: {'YES' if GROQ_API_KEY else 'NO — check .env file'}")
    app.run(debug=True, port=5000)