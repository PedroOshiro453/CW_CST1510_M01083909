"""
Week 9 (Streamlit UI): App navigation + session_state + guard pattern.

Run:
    streamlit run Apps.py
"""

import streamlit as st

from Home import render_home_page


from Dashboard import render_cyber_incidents_page


def init_session_state() -> None:
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "page" not in st.session_state:
        st.session_state.page = "Home (Login/Register)"


def require_login() -> None:
    if not st.session_state.is_logged_in:
        st.warning("You must be logged in to access this page.")
        st.stop()


def main() -> None:
    st.set_page_config(
        page_title="Multi-Domain Intelligence Platform (CW2)",
        page_icon="🧠",
        layout="wide",
    )

    init_session_state()

    with st.sidebar:
        st.title("CW2 Navigation")
        if st.session_state.is_logged_in:
            st.success(f"Logged in as: {st.session_state.username}")
        else:
            st.info("Not logged in")

        options = ["Home (Login/Register)", "Cyber Incidents Dashboard"]
        current = st.session_state.page if st.session_state.page in options else options[0]
        page = st.radio("Go to", options=options, index=options.index(current))
        st.session_state.page = page

    if page == "Home (Login/Register)":
        render_home_page()
        return

    require_login()
    render_cyber_incidents_page()


if __name__ == "__main__":
    main()
