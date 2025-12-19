from pathlib import Path
from typing import Optional

import bcrypt


# Resolve DATA/user.txt relative to this file, regardless of CWD
PROJECT_ROOT = Path(__file__).resolve().parent
USER_FILE = PROJECT_ROOT / "DATA" / "user.txt"

DEFAULT_PASSWORD = "Magic123"

def hash_password(password: str) -> str:
    binary_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(binary_password, salt)
    return hashed.decode("utf-8")


def validate_hash(password: str, hashed: str) -> bool:
    bin_pwd = password.encode("utf-8")
    bin_hash = hashed.encode("utf-8")
    return bcrypt.checkpw(bin_pwd, bin_hash)


def verify_password(password: str, hashed: str) -> bool:
    """Compatibility helper used by the Streamlit app (same as validate_hash)."""
    return validate_hash(password, hashed)

def _ensure_user_file():
    USER_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USER_FILE.exists():
        USER_FILE.touch()


def _load_users():
    _ensure_user_file()
    users = {}
    with USER_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                name, hashed = line.split(",", 1)
                users[name] = hashed
            except ValueError:
                # Skip malformed lines
                continue
    return users


def _save_users(users: dict):
    _ensure_user_file()
    with USER_FILE.open("w", encoding="utf-8") as f:
        for name, hashed in users.items():
            f.write(f"{name},{hashed}\n")


def register_user(username: Optional[str] = None, password: Optional[str] = None) -> bool:
    """Register a new user. Returns True on success, False if username exists.

    If password is empty/omitted, uses DEFAULT_PASSWORD for convenience.
    """
    if username is None:
        username = input("Enter username: ").strip()
    if password is None:
        password = input("Enter password (leave blank for default): ")

    if not username:
        print("Username cannot be empty.")
        return False

    if not password.strip():
        password = DEFAULT_PASSWORD

    users = _load_users()
    if username in users:
        print("Username already exists.")
        return False

    users[username] = hash_password(password)
    _save_users(users)
    return True


def login_user(username: Optional[str] = None, password: Optional[str] = None) -> bool:
    """Validate user credentials against stored hashes. Returns True/False.

    If username/password are not provided, prompts via stdin.
    """
    if username is None:
        username = input("Enter username: ").strip()
    if password is None:
        password = input("Enter password: ")

    users = _load_users()
    hashed = users.get(username)
    if not hashed:
        return False
    return validate_hash(password, hashed)