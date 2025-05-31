from flask import Flask, request, jsonify
from main import run_benchmark

app = Flask(__name__)

@app.route("/run-benchmark", methods=["POST"])
def run():
    try:
        run_benchmark()
        return jsonify({"status": "Benchmark completed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
