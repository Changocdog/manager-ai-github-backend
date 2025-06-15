from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.json
    user_prompt = data.get("prompt", "")
    if not user_prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Manager AI for a GitHub dashboard. Respond clearly and suggest commands when possible."},
                {"role": "user", "content": user_prompt}
            ]
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
