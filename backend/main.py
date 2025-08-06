# Step 1: Setup FastApi for backend

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agents import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()

# Step 2: Receive and validate request form Frontend
class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)
    return {
        "response": final_response,
        "tool_called": tool_called_name
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
