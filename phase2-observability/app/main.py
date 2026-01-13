from fastapi import FastAPI
import time
import os

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/slow")
def slow():
    time.sleep(5)
    return {"status": "slow response"}

@app.get("/crash")
def crash():
    os._exit(1)

@app.get("/")
def root():
    return {"message": "observability demo app"}
