---
title: PR Review Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🤖 PR Review Agent

A free, open-source GitHub Pull Request Review Agent built with **Gradio + GitHub REST API + Docker**, deployed live on **Hugging Face Spaces** — no paid APIs required!

---

## 🌐 Live Demo

👉 [https://huggingface.co/spaces/Keerthana89/pr-review-env](https://huggingface.co/spaces/Keerthana89/pr-review-env)

---

## 📌 What It Does

Paste any **public GitHub PR URL** and instantly get:

- 📌 PR title, author, branch info, and status
- 📁 List of all changed files (added / modified / deleted)
- ➕➖ Additions and deletions count per file
- 🔍 Actual code diff preview line by line
- 🔒 Supports private repos via GitHub Token

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core language |
| Gradio | Web UI framework |
| GitHub REST API | Fetch PR data (free) |
| Docker | Containerize the app |
| Hugging Face Spaces | Live cloud deployment |

---

## 📁 Project Structure
```
pr-review-env/
│
├── app.py              # Main Gradio app + GitHub API logic
├── Dockerfile          # Docker container configuration
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ How It Works
```
User pastes GitHub PR URL
        ↓
App parses owner / repo / PR number
        ↓
Calls GitHub REST API (free, no auth needed for public repos)
        ↓
Fetches PR metadata + changed files + diffs
        ↓
Gradio UI displays everything cleanly
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- Git

### Steps

**1. Clone the repo:**
```bash
git clone https://github.com/keerthanakh89/pr-review-env
cd pr-review-env
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the app:**
```bash
python app.py
```

**4. Open in browser:**
```
http://localhost:7860
```

---

## 🐳 Run with Docker

**1. Build the image:**
```bash
docker build -t pr-review-agent .
```

**2. Run the container:**
```bash
docker run -p 7860:7860 pr-review-agent
```

**3. Open in browser:**
```
http://localhost:7860
```

---

## 📖 How to Use

1. Go to the **Live Demo** link above
2. Paste any public GitHub PR URL, for example:
```
https://github.com/facebook/react/pull/28000
```
3. (Optional) Add a GitHub Token for private repos
4. Click **"🔍 Fetch PR Diff"**
5. View the full PR details and code diff instantly!

---

## 📊 Example Output
```
📌 PR #28000: Convert ReactFreshMultipleRenderer to createRoot
👤 Author: eps1lon
🔀 eps1lon:test/create-root → facebook:main
📊 Status: CLOSED
💬 Description: No description provided

📁 Changed Files (1):
==================================================
🟡 packages/react-refresh/src/__tests__/ReactFreshMultipleRenderer.js [modified]
   +7 additions, -3 deletions

   Diff Preview:
   -const ReactDOM = require('react-dom');
   +const ReactDOMClient = require('react-dom/client');
   +const act = require('internal-test-utils').act;
```

---

## 🔑 GitHub Token (Optional)

A token is only needed for **private repos**. For public repos, no token is required.

To get a free GitHub token:
1. Go to 👉 [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token"**
3. Select **"repo"** scope
4. Copy and paste into the Token field in the app

---

## 🤝 Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/keerthanakh89">
        <img src="https://github.com/keerthanakh89.png" width="100px;" alt="Keerthana"/>
        <br />
        <b>Keerthana K H</b>
      </a>
      <br />
      Project Lead & Developer
    </td>
    <td align="center">
      <a href="https://github.com/Harshagowdasv">
        <img src="https://github.com/Harshagowdasv.png" width="100px;" alt="Harsha"/>
        <br />
        <b>Harsha Gowda S V</b>
      </a>
      <br />
      Contributor
    </td>
  </tr>
</table>

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Gradio](https://gradio.app/) — for the amazing UI framework
- [GitHub REST API](https://docs.github.com/en/rest) — for free PR data access
- [Hugging Face Spaces](https://huggingface.co/spaces) — for free cloud hosting
- [OpenEnv](https://openenv.dev/) — for the environment framework

---

⭐ If you found this useful, please **star the repo**!