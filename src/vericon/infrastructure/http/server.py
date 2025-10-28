from fastapi import FastAPI
import uvicorn

from vericon.infrastructure.boot import boot

# from pathlib import Path
# from dotenv import load_dotenv

# Load environment variables from project root (.env next to Dockerfile)
# ROOT_DIR = Path(__file__).resolve().parents[3]
# load_dotenv(ROOT_DIR / ".env")

app = FastAPI(title="Vericon API", version="1.0.0")

@app.get("/health")
async def health_check():
    boot()
    """Simple health endpoint to verify container responsiveness."""
    return {"status": "ok", "service": "vericon"}

# Uvicorn entrypoint (used when container CMD executes)
if __name__ == "__main__":
    uvicorn.run(
        "vericon.infrastructure.http.server:app",
        host="0.0.0.0",
        port=int(8080),
        reload=False,
        log_level="info"
    )
