from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

app = FastAPI()

# ✅ Enable CORS so your frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Optional: restrict to your domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/command")
async def process_command(req: Request):
    try:
        body = await req.json()
        prompt = body.get("prompt", "").strip()
        key = body.get("key", "").strip()

        if not prompt or not key:
            return {"response": "❌ Missing prompt or key."}

        # 🔁 Send to OpenRouter (GPT 3.5)
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Manager AI, a powerful assistant that responds helpfully and can return JavaScript commands in this format:\n```js\n/* some code here */\n```"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        data = res.json()
        text = data["choices"][0]["message"]["content"]

        # ✂️ Extract any JS code between ```js ... ```
        import re
        match = re.search(r"```js\n(.*?)```", text, re.DOTALL)
        js_code = match.group(1) if match else None

        return {
            "response": text,
            "command": js_code
        }

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}

# 🚀 Run the app (Render auto-detects PORT)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
