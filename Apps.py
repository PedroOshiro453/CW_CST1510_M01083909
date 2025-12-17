import time
import streamlit as st
from app.incidents import migrating_cyber_incidents
from app.db import get_db_connection
from app.auth import authenticate, register



st.set_page_config(page_title="Home Page", page_icon="🏠", layout="wide")


if 'logged_in' not in st.session_state:
st.session_state.logged_in = False
st.session_state.username = None


def safe_rerun() -> None:
"""Trigger a Streamlit rerun. Use experimental_rerun if present, otherwise
fall back to changing query params which causes a reload."""
if hasattr(st, "experimental_rerun"):
try:
st.experimental_rerun()
return
except Exception:
pass
st.query_params = {"_r": [str(int(time.time()))]}

tab_names = ["Apps"]
if st.session_state.logged_in:
tab_names.append("Dashboard")

tabs = st.tabs(tab_names)

apps_tab = tabs[0]

with apps_tab:
st.header('Authentication')
if not st.session_state.logged_in:
mode = st.radio('Choose action', ['Login', 'Register'], horizontal=True)
if mode == 'Login':
user = st.text_input('Username', key='login_user')
pwd = st.text_input('Password', type='password', key='login_pwd')
if st.button('Login'):
if authenticate(user, pwd):
st.session_state.logged_in = True
st.session_state.username = user
safe_rerun()
else:
st.error('Invalid username or password')
else:
r_user = st.text_input('Choose username', key='reg_user')
r_pwd = st.text_input('Choose password', type='password', key='reg_pwd')
if st.button('Register'):
if not r_user or not r_pwd:
st.error('Please provide username and password')
else:
ok = register(r_user, r_pwd)
if ok:
st.success('Registered successfully — please login')
else:
st.error('Username already exists')
else:
st.success(f"Logged in as {st.session_state.username}")
if st.button('Logout'):
st.session_state.logged_in = False
st.session_state.username = None
safe_rerun()

if st.session_state.logged_in:
dashboard_tab = tabs[1]
with dashboard_tab:
st.header('Home Page')
st.write(f'Welcome {st.session_state.username} — to the Home Page of the Application!')

conn = get_db_connection()
data = migrating_cyber_incidents(conn)

st.subheader('Cyber Incidents Overview')
severity_ = st.selectbox('severity', data['severity'].unique())

filtered_data = data[data['severity'] == severity_]

col1, col2 = st.columns(2)
with col1:
st.subheader('Number of Incidents by Severity')
st.bar_chart(filtered_data['category'].value_counts())

with col2:
st.subheader('Filtered Cyber Incidents Data')
st.line_chart(filtered_data, x='timestamp', y='incident_id')

st.dataframe(filtered_data)



if not st.session_state.logged_in:
st.title('Please sign in')
st.info('Use the sidebar to login or register.')
st.stop()


st.header('Home Page')
st.write(f'Welcome {st.session_state.username} — to the Home Page of the Application!')

conn = get_db_connection()
data = migrating_cyber_incidents(conn)

with st.sidebar:
st.header('Cyber Incidents Overview')
severity_ = st.selectbox('severity', data['severity'].unique())

filtered_data = data[data['severity'] == severity_]

col1, col2 = st.columns(2)
with col1:
st.subheader('Number of Incidents by Severity')
st.bar_chart(filtered_data['category'].value_counts())

with col2:
st.subheader('Filtered Cyber Incidents Data')
st.line_chart(filtered_data, x='timestamp', y='incident_id')

st.dataframe(filtered_data)