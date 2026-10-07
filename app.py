import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="System-Health-Mindset",
    version="1.0.0",
    description="Core application logic for System-Health-Mindset"
)

@app.get("/")
def read_root():
    return {"status": "online", "system": "System-Health-Mindset Active"}

@app.get("/health")
def health_check():
    return JSONResponse(status_code=200, content={"health": "optimal"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
