import pandas as pd

# Load dataset
df = pd.read_csv("ball_by_ball_ipl.csv")


# ---------- BATSMAN STATS ----------
def get_batsman_stats(batsman):

    data = df[df["Batter"] == batsman]

    if data.empty:
        return f"No data found for {batsman}"

    runs = data["Batter Runs"].sum()
    balls = data["Valid Ball"].sum()
    dismissals = data["Wicket"].sum()

    strike_rate = (runs / balls) * 100 if balls > 0 else 0
    avg = runs / dismissals if dismissals > 0 else runs

    return f"""
Batsman Analysis: {batsman}

Total Runs: {runs}
Balls Faced: {balls}
Dismissals: {dismissals}
Average: {avg:.2f}
Strike Rate: {strike_rate:.2f}
"""


# ---------- BOWLER STATS ----------
def get_bowler_stats(bowler):

    data = df[df["Bowler"] == bowler]

    if data.empty:
        return f"No data found for {bowler}"

    runs = data["Bowler Runs Conceded"].sum()
    wickets = data["Wicket"].sum()
    balls = data["Valid Ball"].sum()

    overs = balls / 6 if balls > 0 else 0
    economy = runs / overs if overs > 0 else 0

    return f"""
Bowler Analysis: {bowler}

Runs Conceded: {runs}
Wickets Taken: {wickets}
Overs Bowled: {overs:.1f}
Economy Rate: {economy:.2f}
"""


# ---------- MATCHUP STATS ----------
def get_matchup_stats(batsman, bowler):

    data = df[(df["Batter"] == batsman) & (df["Bowler"] == bowler)]

    if data.empty:
        return f"No head-to-head data between {batsman} and {bowler}"

    runs = data["Batter Runs"].sum()
    balls = data["Valid Ball"].sum()
    wickets = data["Wicket"].sum()

    strike_rate = (runs / balls) * 100 if balls > 0 else 0

    return f"""
Head-to-Head Matchup

Batsman: {batsman}
Bowler: {bowler}

Runs Scored: {runs}
Balls Faced: {balls}
Dismissals: {wickets}
Strike Rate: {strike_rate:.2f}
"""


# ---------- BEST BOWLER AGAINST BATSMAN ----------
def best_bowler_against(batsman):

    data = df[df["Batter"] == batsman]

    summary = (
        data.groupby("Bowler")
        .agg({"Wicket": "sum"})
        .sort_values(by="Wicket", ascending=False)
    )

    if summary.empty:
        return f"No data found against {batsman}"

    best = summary.head(5)

    return f"""
Best Bowlers Against {batsman}

{best}
"""


# ---------- BEST BATSMAN AGAINST BOWLER ----------
def best_batsman_against(bowler):

    data = df[df["Bowler"] == bowler]

    summary = (
        data.groupby("Batter")
        .agg({"Batter Runs": "sum"})
        .sort_values(by="Batter Runs", ascending=False)
    )

    if summary.empty:
        return f"No data found against {bowler}"

    best = summary.head(5)

    return f"""
Best Batsmen Against {bowler}

{best}
"""
