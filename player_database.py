import pandas as pd

df = pd.read_csv("ball_by_ball_ipl.csv")


def get_players():

    batsmen = df["Batter"].dropna().unique().tolist()
    bowlers = df["Bowler"].dropna().unique().tolist()

    return batsmen, bowlers
