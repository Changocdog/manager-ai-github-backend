import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                { "role": "system", "content": "You are Manager AI, a helpful assistant that helps manage HTML, code, and backend." },
                { "role": "user", "content": prompt }
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({ "response": reply })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
