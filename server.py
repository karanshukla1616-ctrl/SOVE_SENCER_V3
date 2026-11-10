import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI(title="Telegram Bot Hosting", version="9.0")

HOST_DIR = "hosted_bots"
os.makedirs(HOST_DIR, exist_ok=True)
active_bots = []

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>index.html not found!</h1>"

@app.post("/api/upload-bot")
async def upload_bot(file: UploadFile = File(...), bot_name: str = Form(...)):
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Only .py files are supported.")
    
    file_path = os.path.join(HOST_DIR, file.filename)
    content = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(content)
        
    active_bots.append({"name": bot_name, "file": file.filename})
    return {"status": "success", "message": f"Bot '{bot_name}' successfully hosted!"}

@app.get("/api/bots")
async def get_bots():
    return active_bots

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
