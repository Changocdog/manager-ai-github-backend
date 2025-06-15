from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.json
    prompt = data.get("prompt", "")
    key = data.get("key", "")
    if not prompt or not key:
        return jsonify({"response": "❌ Missing prompt or API key."}), 400

    try:
        openai.api_key = key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Manager AI, a helpful assistant for controlling a web app. Respond with an optional command to run using JavaScript if needed."},
                {"role": "user", "content": prompt}
            ]
        )
        text = response["choices"][0]["message"]["content"]
        
        # Look for ```js code blocks to execute
        command = ""
        if "```js" in text:
            command = text.split("```js")[1].split("```")[0].strip()

        return jsonify({ "response": text, "command": command })
    
    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
