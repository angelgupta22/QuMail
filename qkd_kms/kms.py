# kms.py
"""
QKD Key Management Service (KMS)

Responsibilities:
- Store QKD-generated keys
- Enforce expiration (TTL)
- Support rotation & revocation
- Provide controlled key access to backend services

NOTE:
In-memory storage is used for demo/testing.
Replace KEY_STORE with Redis / Vault in production.
"""

import time
import uuid
from typing import Dict, Optional

# -----------------------------
# Configuration
# -----------------------------
KEY_TTL_SECONDS = 300        # Key validity (5 minutes)
MAX_KEYS = 1000              # Safety limit


# -----------------------------
# In-memory key store
# -----------------------------
# Structure:
# {
#   key_id: {
#       "key": bytes,
#       "created_at": float,
#       "expires_at": float,
#       "active": bool
#   }
# }
KEY_STORE: Dict[str, Dict] = {}


# -----------------------------
# Internal helpers
# -----------------------------
def _cleanup_expired_keys():
    now = time.time()
    expired = [
        key_id for key_id, data in KEY_STORE.items()
        if now > data["expires_at"] or not data["active"]
    ]
    for key_id in expired:
        KEY_STORE.pop(key_id, None)


def _enforce_limits():
    if len(KEY_STORE) > MAX_KEYS:
        # Remove oldest keys
        sorted_keys = sorted(
            KEY_STORE.items(),
            key=lambda item: item[1]["created_at"]
        )
        for key_id, _ in sorted_keys[:len(KEY_STORE) - MAX_KEYS]:
            KEY_STORE.pop(key_id, None)


# -----------------------------
# Public KMS API
# -----------------------------
def store_key(key: bytes) -> str:
    """
    Stores a new key and returns a key_id
    """
    _cleanup_expired_keys()
    _enforce_limits()

    key_id = str(uuid.uuid4())
    now = time.time()

    KEY_STORE[key_id] = {
        "key": key,
        "created_at": now,
        "expires_at": now + KEY_TTL_SECONDS,
        "active": True
    }

    return key_id


def get_key(key_id: str) -> Optional[bytes]:
    """
    Returns the raw key if valid and active
    Intended ONLY for trusted backend services
    """
    _cleanup_expired_keys()

    data = KEY_STORE.get(key_id)
    if not data or not data["active"]:
        return None

    if time.time() > data["expires_at"]:
        KEY_STORE.pop(key_id, None)
        return None

    return data["key"]


def revoke_key(key_id: str) -> bool:
    """
    Revokes a key immediately
    """
    data = KEY_STORE.get(key_id)
    if not data:
        return False

    data["active"] = False
    KEY_STORE.pop(key_id, None)
    return True


def rotate_key(old_key_id: str, new_key: bytes) -> Optional[str]:
    """
    Replaces an existing key with a new one
    """
    revoked = revoke_key(old_key_id)
    if not revoked:
        return None

    return store_key(new_key)


def key_status(key_id: str) -> Optional[dict]:
    """
    Returns metadata only (no raw key)
    """
    data = KEY_STORE.get(key_id)
    if not data:
        return None

    return {
        "key_id": key_id,
        "created_at": data["created_at"],
        "expires_at": data["expires_at"],
        "active": data["active"]
    }
