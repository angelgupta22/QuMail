# api.py
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from crypto import derive_session_key, encrypt_message, decrypt_message

# ---------------- App ----------------
app = FastAPI(title="QuMail Backend Service")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Config ----------------
QKD_KMS_BASE = "http://127.0.0.1:8001"

# ---------------- Models ----------------
class SendRequest(BaseModel):
    message: str

class SendResponse(BaseModel):
    key_id: str
    encrypted_payload: dict

class DecryptRequest(BaseModel):
    key_id: str
    nonce: str
    ciphertext: str

# ---------------- API ----------------
@app.post("/send", response_model=SendResponse)
def send_message(data: SendRequest):
    # 1. Generate QKD key
    r = requests.post(f"{QKD_KMS_BASE}/qkd/generate")
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="QKD key generation failed")

    key_id = r.json()["key_id"]

    # 2. Fetch raw key (internal)
    r2 = requests.get(f"{QKD_KMS_BASE}/qkd/internal/raw/{key_id}")
    if r2.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch QKD key")

    qkd_key = bytes.fromhex(r2.json()["key_hex"])

    # 3. Derive session key
    session_key = derive_session_key(qkd_key)

    # 4. Encrypt message
    encrypted = encrypt_message(session_key, data.message)

    return {
        "key_id": key_id,
        "encrypted_payload": encrypted
    }

@app.post("/decrypt")
def decrypt_payload(data: DecryptRequest):
    # Fetch QKD key
    r = requests.get(f"{QKD_KMS_BASE}/qkd/internal/raw/{data.key_id}")
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Key not found")

    qkd_key = bytes.fromhex(r.json()["key_hex"])

    # Derive session key
    session_key = derive_session_key(qkd_key)

    # Decrypt
    plaintext = decrypt_message(
        session_key,
        data.nonce,
        data.ciphertext
    )

    return {
        "plaintext": plaintext
    }

@app.get("/")
def root():
    return {"status": "Backend running"}
