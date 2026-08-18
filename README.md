# Webhook-to-DOM Execution Engine (`webhook-dom-engine`)

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
