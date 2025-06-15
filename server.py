from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    prompt = data.get("prompt", "")
    key = data.get("key", "")
    
    if not prompt or not key:
        return jsonify({"response": "Missing prompt or key", "command": ""})

    try:
        # Call OpenRouter (OpenAI-compatible API)
        response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Manager AI, an assistant that responds to prompts and can return JavaScript commands to run in a dashboard UI."},
                {"role": "user", "content": prompt}
            ],
            api_key=key,
        )

        content = response.choices[0].message.content

        # If Manager AI includes code in a ```js block, extract it
        command = ""
        if "```js" in content:
            start = content.find("```js") + 5
            end = content.find("```", start)
            command = content[start:end].strip()

        return jsonify({
            "response": content,
            "command": command
        })
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}", "command": ""})

if __name__ == "__main__":
    app.run(debug=True)
