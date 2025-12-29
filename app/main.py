from fastapi import FastAPI, Response, status

app = FastAPI()

is_healthy = True
is_ready = True

@app.get("/")
def root():
    return {
        "message": "Phase 1 app running",
        "healthy": is_healthy,
        "ready": is_ready
    }

@app.post("/break-readiness")
def break_readiness():
    global is_ready
    is_ready = False
    return {"message": "Readiness broken"}

@app.post("/break-liveness")
def break_liveness():
    global is_healthy
    is_healthy = False
    return {"message": "Liveness broken"}

@app.get("/ready")
def readiness(response: Response):
    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready"}
    return {"status": "ready"}

@app.get("/health")
def health(response: Response):
    if not is_healthy:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy"}
    return {"status": "healthy"}
