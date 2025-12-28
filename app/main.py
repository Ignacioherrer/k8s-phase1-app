import os
import time
import signal
import sys
from fastapi import FastAPI
from threading import Event

app = FastAPI()

# Configuration from environment variables
STARTUP_DELAY = int(os.getenv("STARTUP_DELAY", "10"))
RESPONSE_DELAY = float(os.getenv("RESPONSE_DELAY", "0"))
SHUTDOWN_GRACE = int(os.getenv("SHUTDOWN_GRACE", "10"))

ready = False
shutdown_event = Event()


@app.on_event("startup")
def startup_event():
    global ready
    print(f"Starting application. Simulating startup delay: {STARTUP_DELAY}s")
    time.sleep(STARTUP_DELAY)
    ready = True
    print("Application is ready.")


@app.get("/health")
def health():
    return {"status": "alive"}


@app.get("/ready")
def readiness():
    if ready:
        return {"status": "ready"}
    return {"status": "not ready"}


@app.get("/")
def root():
    time.sleep(RESPONSE_DELAY)
    return {"message": "Hello from Kubernetes Phase 1"}


def handle_sigterm(signum, frame):
    global ready
    print("SIGTERM received. Shutting down gracefully...")
    ready = False
    time.sleep(SHUTDOWN_GRACE)
    print("Shutdown complete.")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)
