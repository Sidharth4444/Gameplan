import pandas as pd

# Load dataset
df = pd.read_csv("ball_by_ball_ipl.csv")


def get_batsman_stats(player):

    player_df = df[df["batter"] == player]

    if player_df.empty:
        return "No data available"

    runs = player_df["batsman_runs"].sum()
    balls = len(player_df)
    strike_rate = round((runs / balls) * 100, 2)

    dismissals = player_df["player_dismissed"].dropna()
    outs = dismissals[dismissals == player].count()

    stats = f"""
    Player: {player}
    Total Runs: {runs}
    Balls Faced: {balls}
    Strike Rate: {strike_rate}
    Times Out: {outs}
    """

    return stats
