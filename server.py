from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    prompt = data.get("prompt")
    key = data.get("key")
    if not prompt or not key:
        return jsonify({"response": "❌ Missing prompt or key"}), 400

    openai.api_key = key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Manager AI, a powerful assistant that can control an app and provide code-based commands."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        return jsonify({"response": content})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
