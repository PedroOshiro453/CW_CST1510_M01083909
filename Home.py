"""
Home page: Login / Register (file-based).

Uses:
- DATA/user.txt to store credentials as: username,bcrypt_hash
- bcrypt for password security
- Streamlit session_state for auth status

NOTE:
- Uses st.rerun() (modern Streamlit) instead of st.experimental_rerun()
"""

from __future__ import annotations

from pathlib import Path
import streamlit as st

from log_hash import hash_password, verify_password

DATA_DIR = Path(__file__).parent / "DATA"
USERS_FILE = DATA_DIR / "user.txt"


def ensure_storage() -> None:
    """Ensure the DATA folder and user file exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("", encoding="utf-8")


def read_users() -> dict[str, str]:
    """
    Read users from DATA/user.txt.
    Format per line: username,bcrypt_hash
    """
    ensure_storage()
    users: dict[str, str] = {}
    for line in USERS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or "," not in line:
            continue
        username, pw_hash = line.split(",", 1)
        users[username.strip()] = pw_hash.strip()
    return users


def append_user(username: str, pw_hash: str) -> None:
    """Append a new user to the user file."""
    ensure_storage()
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{pw_hash}\n")


def register_user(username: str, password: str) -> None:
    """Register a new user (raises ValueError on invalid input)."""
    username = username.strip()

    if not username:
        raise ValueError("Username cannot be empty.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")

    users = read_users()
    if username in users:
        raise ValueError("Username already exists.")

    pw_hash = hash_password(password)
    append_user(username, pw_hash)


def login_user(username: str, password: str) -> bool:
    """Validate credentials using the file-based user store."""
    username = username.strip()
    users = read_users()

    if username not in users:
        return False

    return verify_password(password, users[username])


def render_home_page() -> None:
    """Render the Home UI."""
    ensure_storage()

    st.title("🏠 Home (Login / Register)")
    st.caption("Auth source: DATA/user.txt (file-based)")

    # Ensure session keys exist
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login", use_container_width=True):
                if login_user(username, password):
                    st.session_state.is_logged_in = True
                    st.session_state.username = username.strip()
                    st.success("Login successful.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with col2:
            if st.button("Logout", use_container_width=True):
                st.session_state.is_logged_in = False
                st.session_state.username = ""
                st.info("You have been logged out.")
                st.rerun()

        st.write("---")
        st.write("Status:", "✅ Logged in" if st.session_state.is_logged_in else "❌ Not logged in")

    with tab_register:
        st.subheader("Register")

        new_user = st.text_input("New username", key="reg_username")
        new_pwd = st.text_input("New password", type="password", key="reg_password")

        if st.button("Create account"):
            try:
                register_user(new_user, new_pwd)
                st.success("Account created. Now go to the Login tab.")
            except ValueError as e:
                st.error(str(e))
