# api/index.py  (top-level folder named "api")
from fastapi import FastAPI, Response
from app.api.routes import router as routes  # imports your /debate and /health

app = FastAPI(title="kopi-debate-bot")
app.include_router(routes, prefix="")  # exposes /debate and /health inside the function

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)
