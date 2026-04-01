import gradio as gr
import requests
import re

def parse_pr_url(pr_url):
    """Extract owner, repo, PR number from GitHub URL"""
    pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.match(pattern, pr_url.strip())
    if not match:
        return None, None, None
    return match.group(1), match.group(2), match.group(3)

def fetch_pr_details(owner, repo, pr_number, token=None):
    """Fetch PR metadata"""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        return None, "❌ PR not found. Make sure the URL is correct and the repo is public."
    if response.status_code == 403:
        return None, "❌ Rate limit hit. Add a GitHub token to increase limits."
    if response.status_code != 200:
        return None, f"❌ GitHub API error: {response.status_code}"
    
    return response.json(), None

def fetch_pr_files(owner, repo, pr_number, token=None):
    """Fetch list of changed files"""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None, f"❌ Could not fetch files: {response.status_code}"
    
    return response.json(), None

def review_pr(pr_url, github_token):
    if not pr_url.strip():
        return "⚠️ Please enter a GitHub PR URL."
    
    # Parse URL
    owner, repo, pr_number = parse_pr_url(pr_url)
    if not owner:
        return "❌ Invalid PR URL. Format: https://github.com/owner/repo/pull/123"
    
    token = github_token.strip() if github_token.strip() else None
    
    # Fetch PR details
    pr_data, error = fetch_pr_details(owner, repo, pr_number, token)
    if error:
        return error
    
    # Fetch changed files
    files_data, error = fetch_pr_files(owner, repo, pr_number, token)
    if error:
        return error
    
    # Build output
    output = []
    output.append(f"📌 PR #{pr_number}: {pr_data['title']}")
    output.append(f"👤 Author: {pr_data['user']['login']}")
    output.append(f"🔀 {pr_data['head']['label']} → {pr_data['base']['label']}")
    output.append(f"📊 Status: {pr_data['state'].upper()}")
    output.append(f"💬 Description: {pr_data['body'] or 'No description provided'}")
    output.append(f"\n📁 Changed Files ({len(files_data)}):")
    output.append("=" * 50)
    
    total_additions = 0
    total_deletions = 0
    
    for f in files_data:
        additions = f.get("additions", 0)
        deletions = f.get("deletions", 0)
        total_additions += additions
        total_deletions += deletions
        status = f.get("status", "modified")
        
        status_icon = {"added": "🟢", "removed": "🔴", "modified": "🟡", "renamed": "🔵"}.get(status, "⚪")
        output.append(f"\n{status_icon} {f['filename']} [{status}]")
        output.append(f"   +{additions} additions, -{deletions} deletions")
        
        # Show patch (diff) if available
        patch = f.get("patch", "")
        if patch:
            output.append(f"\n   Diff Preview:")
            # Show first 20 lines of diff
            diff_lines = patch.split("\n")[:20]
            for line in diff_lines:
                if line.startswith("+"):
                    output.append(f"   {line}")
                elif line.startswith("-"):
                    output.append(f"   {line}")
                else:
                    output.append(f"   {line}")
            if len(patch.split("\n")) > 20:
                output.append(f"   ... ({len(patch.split(chr(10))) - 20} more lines)")
    
    output.append(f"\n{'='*50}")
    output.append(f"📈 Total: +{total_additions} additions, -{total_deletions} deletions across {len(files_data)} files")
    
    return "\n".join(output)

with gr.Blocks(title="PR Review Agent") as demo:
    gr.Markdown("## 🤖 PR Review Agent")
    gr.Markdown("Paste a GitHub PR URL to fetch its diff and file changes.")
    
    with gr.Row():
        pr_input = gr.Textbox(
            label="GitHub PR URL",
            placeholder="https://github.com/owner/repo/pull/123",
            scale=3
        )
        token_input = gr.Textbox(
            label="GitHub Token (optional, for private repos)",
            placeholder="ghp_xxxx",
            type="password",
            scale=1
        )
    
    btn = gr.Button("🔍 Fetch PR Diff", variant="primary")
    output = gr.Textbox(label="PR Review Output", lines=30)
    btn.click(fn=review_pr, inputs=[pr_input, token_input], outputs=output)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )