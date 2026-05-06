"""
axiom-battle Web API Server
=============================
用 FastAPI 包装 axiom-battle 的核心功能，对外提供 REST 接口。

部署：uvicorn api_server:app --host 0.0.0.0 --port $PORT
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
from pathlib import Path

from axiom_battle.axioms import AXIOM_REGISTRY, AXIOM_REGISTRY_V2, AXIOM_REGISTRY_V3
from axiom_battle.axioms.axiom_base import AxiomCase


# ── FastAPI app ─────────────────────────────────────────────

app = FastAPI(
    title="Axiom Battle API",
    description="悟道体系公理对抗赛引擎 REST API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 请求/响应模型 ────────────────────────────────────────────

class RunAxiomRequest(BaseModel):
    axiom_name: str
    version: Optional[int] = 1  # 1=v1, 2=v2, 3=v3


class AttackResult(BaseModel):
    type: str
    description: str
    severity: str
    evidence: str
    expected_impact: str


class AxiomResult(BaseModel):
    name: str
    statement: str
    verdict: str
    survival_pressure: float
    verdict_reason: str
    attacks: list[AttackResult]


# ── 路由 ────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "Axiom Battle API",
        "version": "1.0.0",
        "endpoints": [
            "GET  /health",
            "GET  /axioms",
            "POST /run",
            "GET  /run/{axiom_name}",
        ],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/axioms")
def list_axioms():
    """列出所有可用公理"""
    return {
        "v1": list(AXIOM_REGISTRY.keys()),
        "v2": list(AXIOM_REGISTRY_V2.keys()),
        "v3": list(AXIOM_REGISTRY_V3.keys()),
    }


@app.post("/run", response_model=AxiomResult)
def run_axiom(req: RunAxiomRequest):
    """运行单个公理的对抗验证"""
    registry = {1: AXIOM_REGISTRY, 2: AXIOM_REGISTRY_V2, 3: AXIOM_REGISTRY_V3}.get(req.version, AXIOM_REGISTRY)

    if req.axiom_name not in registry:
        available = list(registry.keys())
        raise HTTPException(status_code=404, detail=f"公理 {req.axiom_name} 未找到，可用: {available}")

    axiom_cls = registry[req.axiom_name]
    case: AxiomCase = axiom_cls().run()

    return AxiomResult(
        name=case.name,
        statement=case.statement,
        verdict=case.verdict,
        survival_pressure=case.survival_pressure,
        verdict_reason=case.verdict_reason or "",
        attacks=[
            AttackResult(
                type=atk.type,
                description=atk.description,
                severity=atk.severity.name,
                evidence=atk.evidence,
                expected_impact=atk.expected_impact,
            )
            for atk in case.attacks
        ],
    )


@app.get("/run/{axiom_name}")
def run_axiom_get(axiom_name: str, version: Optional[int] = 1):
    """GET 方式运行公理（方便浏览器测试）"""
    registry = {1: AXIOM_REGISTRY, 2: AXIOM_REGISTRY_V2, 3: AXIOM_REGISTRY_V3}.get(version, AXIOM_REGISTRY)

    if axiom_name not in registry:
        raise HTTPException(status_code=404, detail=f"公理 {axiom_name} 未找到")

    axiom_cls = registry[axiom_name]
    case: AxiomCase = axiom_cls().run()

    return {
        "name": case.name,
        "statement": case.statement,
        "verdict": case.verdict,
        "survival_pressure": f"{case.survival_pressure:.0%}",
        "verdict_reason": case.verdict_reason or "",
        "attacks": [
            {
                "type": atk.type,
                "description": atk.description,
                "severity": atk.severity.name,
                "evidence": atk.evidence,
                "expected_impact": atk.expected_impact,
            }
            for atk in case.attacks
        ],
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api_server:app", host="0.0.0.0", port=port)