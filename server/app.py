from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import uvicorn
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inference import run

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StepRequest(BaseModel):
    pr_url: str
    token: str = None

env_state = {"last_pr": None, "result": None}

@app.post("/reset")
def reset():
    env_state["last_pr"] = None
    env_state["result"] = None
    return {"status": "reset", "observation": "Environment reset. Ready for PR review."}

@app.post("/step")
def step(req: StepRequest):
    result = run(req.pr_url, req.token)
    env_state["last_pr"] = req.pr_url
    env_state["result"] = result
    return {
        "observation": result,
        "reward": 1.0 if "error" not in result else 0.0,
        "done": True,
        "info": {}
    }

@app.get("/health")
def health():
    return {"status": "ok"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
