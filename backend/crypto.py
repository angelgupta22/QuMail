# crypto.py
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

def derive_session_key(qkd_key: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"QuMail Session Key"
    ).derive(qkd_key)

def encrypt_message(session_key: bytes, plaintext: str) -> dict:
    aes = AESGCM(session_key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, plaintext.encode(), None)

    return {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }

def decrypt_message(session_key: bytes, nonce_b64: str, ciphertext_b64: str) -> str:
    aes = AESGCM(session_key)
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = aes.decrypt(nonce, ciphertext, None)
    return plaintext.decode()
