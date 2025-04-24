# Julep Research API

A FastAPI application that uses the Julep AI platform to research topics and present information in various formats.

## Overview

This project creates a research API that allows users to query topics and receive structured information in different formats:
- Summary (3-4 sentences)
- Bullet points (5 key points)
- Short report (under 150 words)

The application uses Julep's AI agents to gather and structure information from reliable sources like Wikipedia.

## Prerequisites

- Python 3.8+
- [Julep API key](https://julep.ai/) (sign up required)
- FastAPI
- Uvicorn (for local server)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/julep-research-api.git
cd julep-research-api
```

### 2. Set up a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn julep pydantic python-dotenv
```

### 4. Set up environment variables

Create a `.env` file in the project root directory:

```
JULEP_API_KEY=your_julep_api_key_here
```

### 5. Generate agent and task IDs

Before running the main API, you need to create a Julep agent and task:

```bash
python agent.py
```

This will output agent and task IDs that you should copy and paste into the `app.py` file:

```python
# In app.py
AGENT_UUID = "generated_agent_id_here"
TASK_UUID = "generated_task_id_here"
```

### 6. Run the API server

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

## API Usage

### Research Endpoint

**POST /research**

Request body:
```json
{
  "topic": "cristiano ronaldo",
  "format": "summary"
}
```

Valid format values:
- `"summary"`
- `"bullet points"`
- `"short report"`

Example response:
```json
{
  "result": "Cristiano Ronaldo is a Portuguese professional footballer widely regarded as one of the greatest players of all time. Born on February 5, 1985, he has won numerous awards including five Ballon d'Or trophies and holds the record for most goals in international football. Throughout his career, Ronaldo has played for clubs including Sporting CP, Manchester United, Real Madrid, Juventus, and currently Al Nassr in Saudi Arabia."
}
```

## Project Structure

```
julep-research-api/
├── .env                  # Environment variables (not tracked in git)
├── app.py                # FastAPI application
├── agent.py              # Script to generate agent and task IDs
└── README.md             # This file
```

## Troubleshooting

- **API Key Issues**: Ensure your Julep API key is correctly set in the .env file
- **Execution Timeout**: If research takes too long, adjust the timeout in the polling loop
- **Format Errors**: Ensure you're using one of the three supported formats

## License

[MIT License](LICENSE)
