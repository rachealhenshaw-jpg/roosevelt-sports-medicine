import streamlit as st
from supabase import create_client
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Roosevelt Sports Medicine", layout="wide")

# ---------------- SUPABASE CONNECTION ----------------
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
def login_page():

    st.title("🏟️ Roosevelt Sports Medicine")

    st.subheader("Login to Performance System")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                st.session_state.user = res.user
                st.rerun()
            except:
                st.error("Login failed")

    with col2:
        if st.button("Sign Up"):
            try:
                supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                st.success("Account created. Now login.")
            except:
                st.error("Signup failed")

# ---------------- DASHBOARD ----------------
def dashboard():

    st.sidebar.title("Roosevelt Performance OS")

    page = st.sidebar.radio("Navigation", [
        "Dashboard",
        "Athletes",
        "Screening",
        "Rehab",
        "AI Form Check",
        "Logout"
    ])

    if page == "Logout":
        st.session_state.user = None
        st.rerun()

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":

        st.title("📊 Performance Command Center")

        athletes = supabase.table("athletes").select("*").execute().data
        screenings = supabase.table("screenings").select("*").execute().data

        col1, col2, col3 = st.columns(3)

        col1.metric("Athletes", len(athletes))
        col2.metric("Screenings", len(screenings))
        col3.metric("System", "Active")

        st.divider()

        st.subheader("Athlete Overview")

        for a in athletes:
            st.write(f"🏃 {a['name']} | {a['sport']} | {a['status']}")

    # ---------------- ATHLETES ----------------
    elif page == "Athletes":

        st.title("🏃 Athlete Database")

        name = st.text_input("Athlete Name")
        sport = st.text_input("Sport")
        status = st.selectbox("Status", ["Healthy", "Rehab", "Return-to-Play"])

        if st.button("Add Athlete"):

            supabase.table("athletes").insert({
                "name": name,
                "sport": sport,
                "status": status
            }).execute()

            st.success("Athlete added")

    # ---------------- SCREENING ----------------
    elif page == "Screening":

        st.title("🧪 Movement Screening")

        athlete = st.text_input("Athlete Name")

        shoulder = st.slider("Shoulder Score", 0, 6, 3)
        acl = st.slider("ACL Score", 0, 6, 3)

        if st.button("Save Screening"):

            supabase.table("screenings").insert({
                "athlete": athlete,
                "shoulder_score": shoulder,
                "acl_score": acl
            }).execute()

            st.success("Screening saved")

    # ---------------- REHAB ----------------
    elif page == "Rehab":

        st.title("💪 Rehab Tracker")

        athlete = st.text_input("Athlete Name")
        streak = st.number_input("Rehab Streak", 0, 100, 1)

        if st.button("Save Rehab Log"):

            supabase.table("rehab_logs").insert({
                "athlete": athlete,
                "streak": streak
            }).execute()

            st.success("Rehab logged")

    # ---------------- AI FORM CHECK ----------------
    elif page == "AI Form Check":

        st.title("🤖 AI Form Check")

        video = st.file_uploader("Upload Movement Video", type=["mp4", "mov"])

        if video:
            st.video(video)
            st.info("AI analysis placeholder (connect OpenAI next step)")

# ---------------- APP ROUTER ----------------
if st.session_state.user is None:
    login_page()
else:
    dashboard()
