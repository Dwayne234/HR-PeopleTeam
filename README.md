# GenAI Research Assistant

A Streamlit-based AI research assistant that can answer questions about Transformers, Attention Mechanisms, and recent ML papers.

## Features

- Interactive chat interface
- Export chat history as JSON or Text
- Clear chat functionality
- Timestamps for all messages
- Responsive UI

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export GENAI_API_URL=your_api_url
export AGENT_ACCESS_KEY=your_access_key
```

3. Run the app:
```bash
streamlit run main.py
```

## Deployment

This app is configured to run on DigitalOcean App Platform with the following settings:
- Run command: `streamlit run main.py --server.port $PORT --server.enableCORS false`
- Python environment
- Required environment variables: `GENAI_API_URL`, `AGENT_ACCESS_KEY` 