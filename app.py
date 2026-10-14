from flask import Flask, render_template, request, jsonify
from agent import run_agent
from llm import call_llm

print("[NetMind] Flask starting. Gemini will be tested lazily on first request.", flush=True)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/diagnose", methods=["POST"])
def diagnose():
    try:
        data = request.get_json()
        problem = (data or {}).get("problem", "").strip()

        if not problem:
            return jsonify({"error": "Please describe the problem."}), 400

        result = run_agent(problem, call_llm)
        return jsonify(result)
    except Exception as e:
        import traceback
        return jsonify({
            "error": f"{type(e).__name__}: {e}",
            "trace": traceback.format_exc().splitlines()
        }), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)