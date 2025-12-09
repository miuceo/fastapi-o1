import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def main():
    return {
        "message": "Hello from FastAPI!"
    }

if __name__ == "__main__":
    uvicorn.run(app)