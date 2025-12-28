"""
Password Hashing Utilities
"""
import hashlib
import os

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt"""
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + pwd_hash.hex()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    salt = bytes.fromhex(password_hash[:64])
    stored_hash = password_hash[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex() == stored_hash
