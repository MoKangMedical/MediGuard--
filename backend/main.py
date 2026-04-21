#!/usr/bin/env python3
"""
MediGuard医保智盾 - 后端主入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="MediGuard医保智盾",
    description="医保智能风控与合规平台",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "欢迎使用MediGuard医保智盾", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "MediGuard医保智盾"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
