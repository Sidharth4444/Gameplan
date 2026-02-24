from query_parser import extract_players, detect_intent
from performance_engine import (
    get_batsman_stats,
    get_bowler_stats,
    get_matchup_stats,
    best_bowler_against,
    best_batsman_against
)
from llm_explainer import explain_strategy


def process_query(query):

    # ---------- NLP EXTRACTION ----------
    batsman, bowler = extract_players(query)
    intent = detect_intent(query)

    # ---------- DEBUG OUTPUT ----------
    print("\n========== DEBUG INFO ==========")
    print("Query:", query)
    print("Detected Intent:", intent)
    print("Detected Batsman:", batsman)
    print("Detected Bowler:", bowler)
    print("================================\n")

    # ---------- MATCHUP ----------
    if intent == "matchup" and batsman and bowler:
        stats = get_matchup_stats(batsman, bowler)
        return explain_strategy(stats)

    # ---------- BATSMAN ANALYSIS ----------
    if intent == "batsman" and batsman:
        stats = get_batsman_stats(batsman)
        return explain_strategy(stats)

    # ---------- BOWLER ANALYSIS ----------
    if intent == "bowler" and bowler:
        stats = get_bowler_stats(bowler)
        return explain_strategy(stats)

    # ---------- BEST BOWLER RECOMMENDATION ----------
    if intent == "bowler_recommendation" and batsman:
        stats = best_bowler_against(batsman)
        return explain_strategy(stats)

    # ---------- BEST BATSMAN RECOMMENDATION ----------
    if intent == "batsman_recommendation" and bowler:
        stats = best_batsman_against(bowler)
        return explain_strategy(stats)

    return "Please ask a clearer cricket strategy question."
