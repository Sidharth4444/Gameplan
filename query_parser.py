import re
import pandas as pd
from collections import defaultdict
from rapidfuzz import process
from player_database import get_players


# ---------- LOAD PLAYERS ----------
batsmen_list, bowlers_list = get_players()

# ---------- LOAD DATASET ----------
df = pd.read_csv("ball_by_ball_ipl.csv")

player_frequency = df["Batter"].value_counts().to_dict()


# ---------- TEXT CLEAN ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text


# ---------- EXPAND PLAYER NAMES ----------
def expand_player_names(player_list):

    lookup = defaultdict(list)

    for name in player_list:

        parts = name.split()

        # Full name
        lookup[name.lower()].append(name)

        # Last name
        if len(parts) > 1:
            lookup[parts[-1].lower()].append(name)

        # Initial format
        if len(parts) == 2:
            lookup[f"{parts[0][0]} {parts[1]}".lower()].append(name)

    return lookup


batsman_lookup = expand_player_names(batsmen_list)
bowler_lookup = expand_player_names(bowlers_list)


# ---------- SELECT BEST PLAYER ----------
def select_best_player(candidates):

    if len(candidates) == 1:
        return candidates[0]

    return max(candidates, key=lambda x: player_frequency.get(x, 0))


# ---------- SMART MATCH ----------
def smart_match(text, lookup_dict, player_list):

    text = clean_text(text)

    for key in lookup_dict:
        if key in text:
            return select_best_player(lookup_dict[key])

    # Fuzzy fallback
    match = process.extractOne(text, player_list)
    if match and match[1] > 70:
        return match[0]

    return None


# ---------- ROLE AWARE EXTRACTION ----------
def extract_players(query):

    query_clean = clean_text(query)

    batsman = None
    bowler = None

    # ---------- BOWLER RECOMMENDATION ----------
    if any(x in query_clean for x in [
        "best bowler",
        "who should bowl",
        "which bowler",
        "trouble",
        "dismiss",
        "weak against"
    ]):

        # Extract player AFTER keyword
        match = re.search(r"(against|to)\s+(.*)", query_clean)

        if match:
            target = match.group(2)
            batsman = smart_match(target, batsman_lookup, batsmen_list)

        return batsman, None


    # ---------- BATSMAN RECOMMENDATION ----------
    if any(x in query_clean for x in [
        "best batsman",
        "who should face",
        "who dominates",
        "who should bat"
    ]):

        match = re.search(r"(against|face)\s+(.*)", query_clean)

        if match:
            target = match.group(2)
            bowler = smart_match(target, bowler_lookup, bowlers_list)

        return None, bowler


    # ---------- MATCHUP ----------
    pattern = r"(.*?)\s+(against|vs|versus)\s+(.*)"
    match = re.search(pattern, query_clean)

    if match:
        left_text = match.group(1)
        right_text = match.group(3)

        batsman = smart_match(left_text, batsman_lookup, batsmen_list)
        bowler = smart_match(right_text, bowler_lookup, bowlers_list)

        return batsman, bowler


    # ---------- BOWL TO ----------
    if "bowl to" in query_clean:
        parts = query_clean.split("bowl to")
        batsman = smart_match(parts[1], batsman_lookup, batsmen_list)
        return batsman, None


    # ---------- FACE ----------
    if "face" in query_clean:
        parts = query_clean.split("face")
        bowler = smart_match(parts[1], bowler_lookup, bowlers_list)
        return None, bowler


    # ---------- GENERAL MATCH ----------
    batsman = smart_match(query_clean, batsman_lookup, batsmen_list)
    bowler = smart_match(query_clean, bowler_lookup, bowlers_list)

    if batsman == bowler:
        bowler = None

    return batsman, bowler


# ---------- INTENT DETECTION ----------
def detect_intent(query):

    q = query.lower()

    # Bowler recommendation
    if any(x in q for x in [
        "who should bowl",
        "best bowler",
        "which bowler",
        "dismiss",
        "trouble",
        "weak against"
    ]):
        return "bowler_recommendation"

    # Batsman recommendation
    if any(x in q for x in [
        "who should face",
        "best batsman",
        "who dominates",
        "who should bat"
    ]):
        return "batsman_recommendation"

    # Matchup
    if any(x in q for x in [
        "against",
        "vs",
        "versus",
        "matchup",
        "head to head"
    ]):
        return "matchup"

    # Batsman performance
    if any(x in q for x in [
        "runs",
        "strike rate",
        "batting",
        "performance"
    ]):
        return "batsman"

    # Bowler performance
    if any(x in q for x in [
        "wickets",
        "economy",
        "bowling"
    ]):
        return "bowler"

    return "unknown"
