from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

OLLAMA_URL = "http://localhost:11434"


class QueryRequest(BaseModel):
    prompt: str
    model: str = "llama3"


@app.get("/query")
async def query(request: QueryRequest):
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": request.model, "prompt": request.prompt, "stream": False},
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    import uvicorn
    port = 9000
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=port)