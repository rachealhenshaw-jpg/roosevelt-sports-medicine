import streamlit as st
from supabase import create_client
import random

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

# ---------------- AI READINESS ENGINE ----------------
def calculate_readiness(shoulder, acl, rehab_streak):

    base = (shoulder + acl) * 10
    bonus = rehab_streak * 2

    score = min(100, base + bonus)

    if score >= 80:
        risk = "LOW"
    elif score >= 50:
        risk = "MODERATE"
    else:
        risk = "HIGH"

    return score, risk

# ---------------- DASHBOARD ----------------
def dashboard():

    st.sidebar.title("Performance OS")

    page = st.sidebar.radio("Navigation", [
        "Dashboard",
        "Athletes",
        "Athlete Profile",
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

        col1, col2, col3 = st.columns(3)

        col1.metric("Athletes", len(athletes))
        col2.metric("System Status", "ACTIVE")
        col3.metric("AI Engine", "v2 LIVE")

        st.divider()

        st.subheader("🔥 Athlete Readiness Snapshot")

        for a in athletes:
            score = a.get("readiness_score", random.randint(40, 95))
            risk = a.get("risk_level", "UNKNOWN")

            st.markdown(f"""
            **🏃 {a['name']}**  
            Sport: {a['sport']}  
            Readiness: `{score}/100`  
            Risk Level: `{risk}`
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
                "status": "Active",
                "readiness_score": 50,
                "risk_level": "UNKNOWN"
            }).execute()

            st.success("Athlete added")

    # ---------------- ATHLETE PROFILE ----------------
    elif page == "Athlete Profile":

        st.title("📄 Athlete Performance Profile")

        athletes = supabase.table("athletes").select("*").execute().data

        names = [a["name"] for a in athletes]
        selected = st.selectbox("Select Athlete", names)

        athlete = next(a for a in athletes if a["name"] == selected)

        st.subheader(f"🏃 {athlete['name']}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Sport", athlete["sport"])
            st.metric("Readiness Score", athlete.get("readiness_score", 50))

        with col2:
            st.metric("Risk Level", athlete.get("risk_level", "UNKNOWN"))

        st.line_chart({
            "Load": [60, 65, 70, 68, 75],
            "Recovery": [70, 72, 74, 78, 80]
        })

    # ---------------- SCREENING ----------------
    elif page == "Screening":

        st.title("🧪 AI Movement Screening v2")

        athlete = st.text_input("Athlete Name")

        shoulder = st.slider("Shoulder Score", 0, 6, 3)
        acl = st.slider("ACL Score", 0, 6, 3)
        rehab = st.slider("Rehab Consistency", 0, 10, 5)

        if st.button("Run AI Assessment"):

            score, risk = calculate_readiness(shoulder, acl, rehab)

            st.success(f"Readiness Score: {score}/100")
            st.warning(f"Risk Level: {risk}")

            supabase.table("screenings").insert({
                "athlete": athlete,
                "shoulder_score": shoulder,
                "acl_score": acl
            }).execute()

    # ---------------- REHAB ----------------
    elif page == "Rehab":

        st.title("💪 Rehab System")

        athlete = st.text_input("Athlete Name")
        streak = st.number_input("Rehab Streak", 0, 100, 1)

        if st.button("Log Rehab"):

            supabase.table("rehab_logs").insert({
                "athlete": athlete,
                "streak": streak
            }).execute()

            st.success("Logged")

    # ---------------- AI ----------------
    elif page == "AI Form Check":

        st.title("🤖 AI Movement Analysis")

        video = st.file_uploader("Upload Video", type=["mp4", "mov"])

        if video:
            st.video(video)
            st.info("AI engine placeholder (next upgrade = full biomechanics model)")

# ---------------- ROUTER ----------------
if st.session_state.user is None:
    login()
else:
    dashboard()
