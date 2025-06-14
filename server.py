from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # e.g., 'username/repo-name'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.json
    user_prompt = data.get("prompt", "")
    if not user_prompt:
        return jsonify({"error": "Missing prompt"}), 400

    # Generate response using GPT
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Manager AI for a GitHub project. Respond in a friendly tone and provide a code block if needed."},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_text = completion.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "response": response_text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
