FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port 7860 (required by HF Spaces)
EXPOSE 7860

# Critical env var — forces Gradio to bind on all interfaces
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]
```

---

### 📄 `requirements.txt`
```
gradio>=4.0.0