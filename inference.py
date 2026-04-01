import requests
import re

def parse_pr_url(pr_url):
    pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.match(pattern, pr_url.strip())
    if not match:
        return None, None, None
    return match.group(1), match.group(2), match.group(3)

def run(pr_url: str, token: str = None) -> dict:
    owner, repo, pr_number = parse_pr_url(pr_url)
    if not owner:
        return {"error": "Invalid PR URL"}

    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    pr_res = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
        headers=headers
    )
    if pr_res.status_code != 200:
        return {"error": f"GitHub API error: {pr_res.status_code}"}

    files_res = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files",
        headers=headers
    )

    pr_data = pr_res.json()
    files_data = files_res.json() if files_res.status_code == 200 else []

    return {
        "title": pr_data.get("title"),
        "author": pr_data.get("user", {}).get("login"),
        "status": pr_data.get("state"),
        "files_changed": len(files_data),
        "additions": sum(f.get("additions", 0) for f in files_data),
        "deletions": sum(f.get("deletions", 0) for f in files_data),
        "files": [
            {
                "filename": f["filename"],
                "status": f["status"],
                "additions": f["additions"],
                "deletions": f["deletions"],
                "patch": f.get("patch", "")[:500]
            }
            for f in files_data
        ]
    }