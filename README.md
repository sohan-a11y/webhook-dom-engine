# Webhook-to-DOM Execution Engine (`webhook-dom-engine`)

![GitHub License](https://img.shields.io/github/license/sohan-a11y/webhook-dom-engine?style=flat-square)
![GitHub Last Commit](https://img.shields.io/github/last-commit/sohan-a11y/webhook-dom-engine?style=flat-square)
![GitHub Stars](https://img.shields.io/github/stars/sohan-a11y/webhook-dom-engine?style=flat-square)
![GitHub Forks](https://img.shields.io/github/forks/sohan-a11y/webhook-dom-engine?style=flat-square)

[![Skills](https://skillicons.dev/icons?i=python,fastapi,docker)](https://skillicons.dev)


A concurrent FastAPI microservice that accepts macro action webhooks and executes them against a headless Playwright Chromium pool, returning scraped DOM values in JSON.

## Quickstart

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Run the server:
```bash
python app.py
```

3. Test with cURL:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com",
    "actions": [
      { "action": "WAIT_FOR", "selector": ".titleline > a" }
    ],
    "return_selector": ".titleline > a"
  }'
```