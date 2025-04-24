import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from julep import Client

# Initialize FastAPI app
app = FastAPI(title="Julep Research API")

# Load environment variable safely
JULEP_API_KEY = os.environ.get('JULEP_API_KEY')
if not JULEP_API_KEY:
    raise RuntimeError("JULEP_API_KEY environment variable is not set.")

# Set your agent and task UUIDs
AGENT_UUID = "06809d96-a402-7774-8000-d3f5dab62926"  
TASK_UUID = "06809d96-aa13-73bd-8000-62c7b5951bab"  

# Initialize Julep client
client = Client(api_key=JULEP_API_KEY, environment="production")

# Pydantic model for input
class ResearchRequest(BaseModel):
    topic: str
    format: str

# /research endpoint
@app.post("/research")
async def research_topic(request: ResearchRequest):
    valid_formats = ["summary", "bullet points", "short report"]
    if request.format not in valid_formats:
        raise HTTPException(status_code=400, detail=f"Invalid format. Choose from {valid_formats}")

    try:
        # Start execution
        execution = client.executions.create(
            task_id=TASK_UUID,
            input={
                "topic": request.topic,
                "output_format": request.format  # <-- key must match your YAML definition
            }
        )

        # Poll until complete
        for _ in range(30):  # 30 tries * 2s = ~60s timeout
            result = client.executions.get(execution.id)
            if result.status in ["succeeded", "failed", "cancelled"]:
                break
            time.sleep(2)

        if result.status == "succeeded":
            return JSONResponse(content={"result": result.output})
        else:
            raise HTTPException(status_code=500, detail=f"Execution failed. Status: {result.status}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


# Optional: for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)