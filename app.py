import streamlit as st
from supabase import create_client
import random
import datetime

# ---------------- SETUP ----------------
st.set_page_config(page_title="Roosevelt Sports Medicine SaaS", layout="wide")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
def login():

    st.title("🏟️ Roosevelt Sports Medicine")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

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

# ---------------- AI ENGINE v3 ----------------
def ai_engine(jump, sprint, fatigue):

    # Simulated biomechanics + load model
    base_score = (jump * 2) + (sprint * 2) - (fatigue * 3)

    risk_prob = max(0, 100 - base_score + random.randint(-5, 5))

    if risk_prob < 30:
        risk = "LOW"
    elif risk_prob < 60:
        risk = "MODERATE"
    else:
        risk = "HIGH"

    readiness = min(100, max(0, base_score))

    return readiness, risk, risk_prob

# ---------------- DASHBOARD ----------------
def dashboard():

    st.sidebar.title("Performance OS")

    page = st.sidebar.radio("Navigation", [
        "Dashboard",
        "Athletes",
        "Athlete Profile",
        "Performance Testing",
        "AI Risk Engine",
        "Rehab Tracker",
        "Logout"
    ])

    if page == "Logout":
        st.session_state.user = None
        st.rerun()

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":

        st.title("📊 Performance Command Center")

        athletes = supabase.table("athletes").select("*").execute().data

        col1, col2, col3 = st.columns(3)

        col1.metric("Athletes", len(athletes))
        col2.metric("System Status", "ENTERPRISE")
        col3.metric("AI Engine", "v3 LIVE")

        st.divider()

        st.subheader("🔥 Live Athlete Risk Overview")

        for a in athletes:

            st.markdown(f"""
            **🏃 {a['name']}**  
            Sport: {a['sport']}  
            Status: {a.get('status','Active')}  
            ---
            """)

    # ---------------- ATHLETES ----------------
    elif page == "Athletes":

        st.title("🏃 Athlete Database")

        name = st.text_input("Name")
        sport = st.text_input("Sport")

        if st.button("Add Athlete"):

            supabase.table("athletes").insert({
                "name": name,
                "sport": sport,
                "status": "Active"
            }).execute()

            st.success("Added")

    # ---------------- PERFORMANCE TESTING ----------------
    elif page == "Performance Testing":

        st.title("📈 Performance Testing Lab")

        athlete = st.text_input("Athlete Name")

        jump = st.slider("Vertical Jump Score", 0, 100, 50)
        sprint = st.slider("Sprint Score", 0, 100, 50)
        fatigue = st.slider("Fatigue Level", 0, 100, 20)

        if st.button("Save Performance Test"):

            supabase.table("performance_logs").insert({
                "athlete": athlete,
                "jump_score": jump,
                "sprint_score": sprint,
                "fatigue_score": fatigue
            }).execute()

            st.success("Saved")

    # ---------------- AI RISK ENGINE ----------------
    elif page == "AI Risk Engine":

        st.title("🧠 AI Injury Risk Engine v3")

        athlete = st.text_input("Athlete Name")

        jump = st.slider("Jump Power", 0, 100, 50)
        sprint = st.slider("Sprint Power", 0, 100, 50)
        fatigue = st.slider("Fatigue", 0, 100, 20)

        if st.button("Run AI Analysis"):

            readiness, risk, prob = ai_engine(jump, sprint, fatigue)

            st.metric("Readiness Score", f"{readiness}/100")
            st.metric("Injury Risk Level", risk)
            st.metric("Risk Probability", f"{prob}%")

            st.progress(int(readiness))

    # ---------------- ATHLETE PROFILE ----------------
    elif page == "Athlete Profile":

        st.title("📄 Athlete Performance Profile")

        athletes = supabase.table("athletes").select("*").execute().data

        names = [a["name"] for a in athletes]
        selected = st.selectbox("Select Athlete", names)

        logs = supabase.table("performance_logs").select("*").execute().data

        athlete_logs = [l for l in logs if l["athlete"] == selected]

        st.subheader(f"🏃 {selected}")

        if athlete_logs:
            jump_scores = [l["jump_score"] for l in athlete_logs]
            sprint_scores = [l["sprint_score"] for l in athlete_logs]

            st.line_chart({
                "Jump": jump_scores,
                "Sprint": sprint_scores
            })

        else:
            st.info("No performance data yet")

    # ---------------- REHAB ----------------
    elif page == "Rehab Tracker":

        st.title("💪 Rehab System")

        athlete = st.text_input("Athlete Name")
        streak = st.number_input("Rehab Streak", 0, 100, 1)

        if st.button("Log Rehab"):

            supabase.table("rehab_logs").insert({
                "athlete": athlete,
                "streak": streak
            }).execute()

            st.success("Logged")

# ---------------- ROUTER ----------------
if st.session_state.user is None:
    login()
else:
    dashboard()
