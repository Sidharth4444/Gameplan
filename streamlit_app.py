import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gameplan_ai import process_query
from performance_engine import *
from player_database import get_players
from datetime import datetime


# ================= PAGE CONFIG ================= #
st.set_page_config(
    page_title="GamePlan AI",
    page_icon="🏏",
    layout="wide"
)


# ================= LOAD DATA ================= #
df = pd.read_csv("ball_by_ball_ipl.csv")
batsmen_list, bowlers_list = get_players()


# ================= SESSION INIT ================= #
if "chat" not in st.session_state:
    st.session_state.chat = []


# ================= CLEAR CHAT FUNCTION ================= #
def clear_chat():
    st.session_state.chat = []


# ================= CUSTOM CSS ================= #
st.markdown("""
<style>

.main-title{
    font-size:45px;
    font-weight:800;
    color:#F9C74F;
}

.metric-card{
    background: linear-gradient(145deg,#111827,#1f2937);
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 4px 15px rgba(0,0,0,0.5);
}

.chat-user{
    background:#1f2937;
    padding:15px;
    border-radius:15px;
    margin-bottom:10px;
}

.chat-ai{
    background:#111827;
    padding:15px;
    border-radius:15px;
    border-left:4px solid #F9C74F;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)


# ================= HEADER ================= #
st.markdown('<p class="main-title">🏏 GamePlan AI Dashboard</p>', unsafe_allow_html=True)
st.caption("IPL Tactical Intelligence Engine")

st.divider()


# ================= SIDEBAR ================= #
st.sidebar.title("⚙ Control Panel")

selected_tab = st.sidebar.radio(
    "Select Module",
    ["AI Strategy Assistant","Player Analytics","Head-to-Head Dashboard"]
)

st.sidebar.divider()

st.sidebar.success("System Active")
st.sidebar.write(datetime.now().strftime("%H:%M:%S"))


# =========================================================
# 🧠 TAB 1 — AI STRATEGY ASSISTANT
# =========================================================

if selected_tab == "AI Strategy Assistant":

    st.subheader("🎯 Ask Tactical Cricket Questions")

    query = st.text_input(
        "Enter Strategy Query",
        key="query_input",
        on_change=clear_chat
    )

    if st.button("Analyze Strategy"):

        with st.spinner("Running AI Tactical Engine..."):

            response = process_query(query)

            st.session_state.chat.append(("user",query))
            st.session_state.chat.append(("ai",response))


    st.divider()

    for role,text in reversed(st.session_state.chat):

        if role=="user":
            st.markdown(f"<div class='chat-user'><b>You:</b><br>{text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'><b>GamePlan AI:</b><br>{text}</div>", unsafe_allow_html=True)



# =========================================================
# 📊 TAB 2 — PLAYER ANALYTICS
# =========================================================

elif selected_tab == "Player Analytics":

    st.subheader("📊 Player Performance Dashboard")

    player = st.selectbox("Select Batsman", batsmen_list)

    player_df = df[df["Batter"] == player]

    col1,col2,col3 = st.columns(3)

    total_runs = player_df["Batter Runs"].sum()
    balls = player_df["Valid Ball"].sum()
    dismissals = player_df["Wicket"].sum()
    strike_rate = round((total_runs/balls)*100,2) if balls>0 else 0

    col1.metric("Total Runs", total_runs)
    col2.metric("Strike Rate", strike_rate)
    col3.metric("Dismissals", dismissals)


    # ---------- RUN DISTRIBUTION ---------- #
    st.subheader("Run Distribution")

    run_chart = px.histogram(
        player_df,
        x="Batter Runs",
        nbins=7,
        title="Runs Per Ball Distribution"
    )

    st.plotly_chart(run_chart, use_container_width=True)


    # ---------- OVER WISE PERFORMANCE ---------- #
    st.subheader("Performance Over Overs")

    over_stats = player_df.groupby("Over")["Batter Runs"].sum().reset_index()

    line_chart = px.line(
        over_stats,
        x="Over",
        y="Batter Runs",
        markers=True
    )

    st.plotly_chart(line_chart, use_container_width=True)



# =========================================================
# ⚔ TAB 3 — HEAD TO HEAD DASHBOARD
# =========================================================

elif selected_tab == "Head-to-Head Dashboard":

    st.subheader("⚔ Batsman vs Bowler Analysis")

    batsman = st.selectbox("Select Batsman", batsmen_list)
    bowler = st.selectbox("Select Bowler", bowlers_list)

    h2h_df = df[(df["Batter"]==batsman) & (df["Bowler"]==bowler)]

    if len(h2h_df) > 0:

        runs = h2h_df["Batter Runs"].sum()
        balls = h2h_df["Valid Ball"].sum()
        wickets = h2h_df["Wicket"].sum()

        strike = round((runs/balls)*100,2) if balls>0 else 0
        avg = round(runs/wickets,2) if wickets>0 else runs

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Runs Scored", runs)
        c2.metric("Balls Faced", balls)
        c3.metric("Strike Rate", strike)
        c4.metric("Dismissals", wickets)


        # ---------- PIE CHART ---------- #
        st.subheader("Ball Outcome Impact")

        dot_balls = len(h2h_df[h2h_df["Batter Runs"] == 0])
        singles = len(h2h_df[h2h_df["Batter Runs"] == 1])
        boundaries = len(h2h_df[h2h_df["Batter Runs"].isin([4,6])])
        others = len(h2h_df[h2h_df["Batter Runs"].isin([2,3])])
        wickets_count = wickets

        labels = ["Dot Balls","Singles","Boundaries","2s & 3s","Dismissals"]
        values = [dot_balls, singles, boundaries, others, wickets_count]

        pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.45,
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>"
        )])

        pie.update_layout(
            title="Ball Outcome Distribution",
            annotations=[dict(text="Matchup\nImpact", x=0.5, y=0.5, font_size=16, showarrow=False)]
        )

        st.plotly_chart(pie, use_container_width=True)


        # ---------- BALL RESULT CHART ---------- #
        st.subheader("Ball Result Breakdown")

        ball_result = (
            h2h_df["Batter Runs"]
            .value_counts()
            .rename_axis("Runs Per Ball")
            .reset_index(name="Frequency")
            .sort_values("Runs Per Ball")
        )

        bar = px.bar(
            ball_result,
            x="Runs Per Ball",
            y="Frequency",
            labels={"Runs Per Ball":"Runs Per Ball","Frequency":"Frequency"}
        )

        st.plotly_chart(bar, use_container_width=True)

    else:
        st.warning("No head-to-head data found.")
