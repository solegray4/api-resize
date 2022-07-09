from fastapi import Fastapi

app = Fastapi()

@app.get("/ping")
def ping():
    return "pong"