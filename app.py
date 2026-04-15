import streamlit as st
import requests
from supabase import create_client

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Roosevelt Sports Medicine", layout="wide")

# ---------------- SUPABASE ----------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- AI ENDPOINT ----------------
REPLIT_AI_URL = "https://roosevelt-ai-vision--rachealhenshaw.replit.app/analyze"

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = True

# ---------------- NAVIGATION ----------------
page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Athletes",
    "Screening",
    "Rehab",
    "AI Vision"
])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("Roosevelt Sports Medicine Dashboard")

    athletes = supabase.table("athletes").select("*").execute().data
    screenings = supabase.table("screenings").select("*").execute().data

    col1, col2, col3 = st.columns(3)
    col1.metric("Athletes", len(athletes))
    col2.metric("Screenings", len(screenings))
    col3.metric("System", "ACTIVE")

    st.divider()

    st.subheader("Athletes")
    for a in athletes:
        st.write(f"{a['name']} - {a['sport']} - {a['status']}")

# ---------------- ATHLETES ----------------
elif page == "Athletes":

    st.title("Athlete Database")

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

    st.title("Movement Screening")

    athlete = st.text_input("Athlete Name")

    shoulder = st.slider("Shoulder Score", 0, 6, 3)
    acl = st.slider("ACL Score", 0, 6, 3)

    if st.button("Save Screening"):

        supabase.table("screenings").insert({
            "athlete": athlete,
            "shoulder_score": shoulder,
            "acl_score": acl
        }).execute()

        st.success("Saved")

# ---------------- REHAB ----------------
elif page == "Rehab":

    st.title("Rehab Tracker")

    athlete = st.text_input("Athlete Name")
    streak = st.number_input("Rehab Streak", 0, 100, 1)

    if st.button("Save Rehab"):

        supabase.table("rehab_logs").insert({
            "athlete": athlete,
            "streak": streak
        }).execute()

        st.success("Saved")

# ---------------- AI VISION ----------------
elif page == "AI Vision":

    st.title("AI Movement Analysis Engine")

    athlete = st.text_input("Athlete Name")

    video = st.file_uploader(
        "Upload Video/Image",
        type=["mp4", "mov", "jpg", "png"]
    )

    if video:

        st.video(video)

        if st.button("Run AI Analysis"):

            try:
                with st.spinner("Analyzing movement with AI Vision..."):

                    # FIXED FILE FORMAT (IMPORTANT)
                    files = {
                        "file": (video.name, video.getvalue(), video.type)
                    }

                    response = requests.post(
                        REPLIT_AI_URL,
                        files=files
                    )

                    if response.status_code == 200:

                        try:
                            result = response.json()
                        except:
                            st.error("Invalid response from AI server")
                            st.stop()

                        st.success("AI Analysis Complete")

                        st.metric("Injury Risk Score", result["injury_risk_score"])
                        st.metric("Risk Level", result["risk_level"])

                        # SAVE TO SUPABASE (CLEAN TABLE DESIGN)
                        supabase.table("ai_results").insert({
                            "athlete": athlete,
                            "risk_score": result["injury_risk_score"],
                            "risk_level": result["risk_level"]
                        }).execute()

                    else:
                        st.error("AI server error")

            except Exception as e:
                st.error(f"Connection failed: {e}")
