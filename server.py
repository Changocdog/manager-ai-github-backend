from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    # This is a placeholder response, you can later integrate GPT-4 here
    response = f"🧠 Manager AI received your request: '{message}'. (Backend is ready for extension.)"
    return jsonify({"reply": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
