from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "Bonjour."

@app.route("/code", methods=["GET"])
def compile_code():
    code = request.args.get("input")

    if not code:
        return jsonify({"error": "Parâmetro 'input' é necessário."}), 400

    try:
        # Detectando se o código é Python ou JavaScript baseado na sintaxe
        if code.strip().startswith("print") or code.strip().startswith("import"):
            # Python
            result = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=5)
        else:
            # JavaScript
            result = subprocess.run(["node", "-e", code], capture_output=True, text=True, timeout=5)

        return jsonify({"output": result.stdout.strip(), "error": result.stderr.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
