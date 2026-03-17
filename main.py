import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os

app = FastAPI()
OLLAMA_URL = "http://localhost:11434"
gemma_model = "gemma3:270m"

async def make_sure_i_have_ollama_gemma():
    os.system(f"curl -fsSL https://ollama.com/install.sh | sh")
    os.system(f"ollama pull {gemma_model}")
    
def is_ollama_and_gemma_installed_():
    return os.system("ollama --version") == 0 and os.system(f"ollama list | grep {gemma_model}") == 0


if not is_ollama_and_gemma_installed_():
    make_sure_i_have_ollama_gemma()


class QueryRequest(BaseModel):
    prompt: str


@app.post("/query")
async def query(request: QueryRequest):
    result = subprocess.run(
        ["ollama", "run", gemma_model, request.prompt],
        capture_output=True,
        text=True
    )
    return {"status": "ok", "response": result.stdout.strip()}


if __name__ == "__main__":
    import uvicorn
    port = 9000
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=port)