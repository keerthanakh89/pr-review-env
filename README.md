---
title: pr-review-env
sdk: docker
app_file: app.py
---
# PR Review OpenEnv (FULL FINAL)

## Features
- Real-world PR review simulation
- OpenAI integration
- HF Space UI (Gradio)
- 3 tasks (easy → hard)
- Reward-based scoring

## Setup
export API_BASE_URL=...
export MODEL_NAME=...
export HF_TOKEN=...

pip install -r requirements.txt
python inference.py

## Deploy HF
Upload to HuggingFace Space with Docker
