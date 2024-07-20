import uvicorn
from src.core import DEBUG

if __name__ == "__main__":
    uvicorn.run(
        host="127.0.0.1",
        port=8000,
        reload=True,
        app="src.core:app",
    )