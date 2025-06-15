from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# Secure API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                { "role": "system", "content": "You are Manager AI, a helpful assistant for managing HTML, code, and app features." },
                { "role": "user", "content": prompt }
            ]
        )
        reply = completion.choices[0].message.content
        return jsonify({ "response": reply })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
