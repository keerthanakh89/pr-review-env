import gradio as gr
import requests
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from inference import run

# ── FastAPI app with OpenEnv endpoints ──────────────────────────────
api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StepRequest(BaseModel):
    pr_url: str
    token: str = None

env_state = {"last_pr": None, "result": None}

@api.post("/reset")
def reset():
    env_state["last_pr"] = None
    env_state["result"] = None
    return {"status": "reset", "observation": "Environment reset. Ready for PR review."}

@api.post("/step")
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

@api.get("/health")
def health():
    return {"status": "ok"}

# ── Gradio UI ────────────────────────────────────────────────────────
def review_pr(pr_url, github_token):
    if not pr_url.strip():
        return "⚠️ Please enter a GitHub PR URL."
    token = github_token.strip() if github_token.strip() else None
    result = run(pr_url, token)

    if "error" in result:
        return f"❌ {result['error']}"

    output = []
    output.append(f"📌 PR: {result['title']}")
    output.append(f"👤 Author: {result['author']}")
    output.append(f"📊 Status: {result['status'].upper()}")
    output.append(f"📁 Files Changed: {result['files_changed']}")
    output.append(f"➕ Additions: {result['additions']}  ➖ Deletions: {result['deletions']}")
    output.append("\n" + "="*50)

    for f in result["files"]:
        status_icon = {"added": "🟢", "removed": "🔴", "modified": "🟡", "renamed": "🔵"}.get(f["status"], "⚪")
        output.append(f"\n{status_icon} {f['filename']} [{f['status']}]")
        output.append(f"   +{f['additions']} additions, -{f['deletions']} deletions")
        if f["patch"]:
            output.append("   Diff Preview:")
            for line in f["patch"].split("\n")[:15]:
                output.append(f"   {line}")

    return "\n".join(output)

with gr.Blocks(title="PR Review Agent") as demo:
    gr.Markdown("## 🤖 PR Review Agent")
    gr.Markdown("Paste a GitHub PR URL to fetch its diff and file changes.")
    with gr.Row():
        pr_input = gr.Textbox(label="GitHub PR URL", placeholder="https://github.com/owner/repo/pull/123", scale=3)
        token_input = gr.Textbox(label="GitHub Token (optional)", placeholder="ghp_xxxx", type="password", scale=1)
    btn = gr.Button("🔍 Fetch PR Diff", variant="primary")
    output = gr.Textbox(label="PR Review Output", lines=30)
    btn.click(fn=review_pr, inputs=[pr_input, token_input], outputs=output)

# ── Mount Gradio into FastAPI ────────────────────────────────────────
from gradio.routes import mount_gradio_app
app = mount_gradio_app(api, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)