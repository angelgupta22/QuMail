# api.py
"""
QKD Key Management Service API

Exposes REST endpoints to:
- Generate simulated QKD keys (BB84)
- Query key status
- Revoke keys

This service is INTERNAL and should NOT be exposed publicly.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bb84 import generate_qkd_key
from kms import store_key, get_key, revoke_key, key_status

app = FastAPI(
    title="QuMail QKD Key Management Service",
    description="Simulated BB84-based QKD Key Generator for Hybrid Secure Systems",
    version="1.0.0"
)

# -----------------------------
# Request / Response Models
# -----------------------------
class GenerateKeyResponse(BaseModel):
    key_id: str
    key_length_bits: int
    status: str


class KeyStatusResponse(BaseModel):
    key_id: str
    created_at: float
    expires_at: float
    active: bool


# -----------------------------
# API Endpoints
# -----------------------------

@app.post("/qkd/generate", response_model=GenerateKeyResponse)
def generate_key():
    """
    Generate a new simulated QKD key using BB84
    """
    try:
        key = generate_qkd_key()
        key_id = store_key(key)
        return GenerateKeyResponse(
            key_id=key_id,
            key_length_bits=len(key) * 8,
            status="active"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/qkd/status/{key_id}", response_model=KeyStatusResponse)
def get_key_status(key_id: str):
    """
    Get metadata/status of a key (no raw key exposure)
    """
    status = key_status(key_id)
    if not status:
        raise HTTPException(status_code=404, detail="Key not found")

    return KeyStatusResponse(**status)


@app.post("/qkd/revoke/{key_id}")
def revoke_existing_key(key_id: str):
    """
    Revoke a key immediately
    """
    success = revoke_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")

    return {
        "key_id": key_id,
        "status": "revoked"
    }


# -----------------------------
# INTERNAL USE ONLY (optional)
# -----------------------------
@app.get("/qkd/internal/raw/{key_id}")
def get_raw_key_internal(key_id: str):
    """
    INTERNAL endpoint for trusted backend services
    DO NOT expose publicly
    """
    key = get_key(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found or expired")

    return {
        "key_id": key_id,
        "key_hex": key.hex()
    }
