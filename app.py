import gradio as gr

def review_pr(pr_url):
    if not pr_url.strip():
        return "⚠️ Please enter a PR URL."
    return f"✅ PR Review Agent received: {pr_url}\n\n(Agent logic goes here)"

with gr.Blocks(title="PR Review Agent") as demo:
    gr.Markdown("## 🤖 PR Review Agent")
    pr_input = gr.Textbox(label="GitHub PR URL", placeholder="https://github.com/owner/repo/pull/123")
    output = gr.Textbox(label="Review Output", lines=10)
    btn = gr.Button("Review PR")
    btn.click(fn=review_pr, inputs=pr_input, outputs=output)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",   # ← CRITICAL: bind to all interfaces
        server_port=7860          # ← CRITICAL: must be exactly 7860
    )