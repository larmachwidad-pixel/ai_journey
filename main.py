from fastapi import FastAPI, PlainTextResponse
from pydantic import BaseModel
from typing import Optional
import os
import json

app = FastAPI(title="Atlas Lions & Cross-Era World Cup Engine")

# Path to our World Cup JSON database
DATA_FILE = "data/worldcup_goals.json"

def init_database():
    # We force-recreate it this time to inject our new Moroccan data fields!
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    extended_data = [
        {
            "player": "Youssef En-Nesyri",
            "year": 2022,
            "minute": 42,
            "stage": "Quarter-Final",
            "opponent": "Portugal",
            "goal_description": "The historic towering header, jumping 2.78 meters into the sky to send Morocco to the Semi-Finals.",
            "era_avg_goals_per_game": 2.69,
            "team_possession_pct": 27.0  # Masterclass in defensive defiance
        },
        {
            "player": "Abderrazak Khairi",
            "year": 1986,
            "minute": 19,
            "stage": "Group Stage",
            "opponent": "Portugal",
            "goal_description": "A brilliant long-range strike that sparked a historic 3-1 win, making Morocco the first African nation to top a WC group.",
            "era_avg_goals_per_game": 2.54,
            "team_possession_pct": 38.0
        },
        {
            "player": "Pelé",
            "year": 1958,
            "minute": 90,
            "stage": "Final",
            "opponent": "Sweden",
            "goal_description": "Brilliant volley to seal the championship",
            "era_avg_goals_per_game": 5.38,
            "team_possession_pct": 55.0
        },
        {
            "player": "Diego Maradona",
            "year": 1986,
            "minute": 55,
            "stage": "Quarter-Final",
            "opponent": "England",
            "goal_description": "The Goal of the Century after dribbling past 5 players",
            "era_avg_goals_per_game": 2.54,
            "team_possession_pct": 52.0
        },
        {
            "player": "Kylian Mbappé",
            "year": 2022,
            "minute": 81,
            "stage": "Final",
            "opponent": "Argentina",
            "goal_description": "Stunning first-time volley to equalize in 97 seconds",
            "era_avg_goals_per_game": 2.69,
            "team_possession_pct": 46.0
        }
    ]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(extended_data, f, indent=4, ensure_ascii=False)

# Run database initializer
init_database()

@app.get("/")
def home():
    return {
        "message": "Welcome to the Moroccan Milestone & Cross-Era Analytics Engine!",
        "status": "Online",
        "docs_url": "/docs"
    }

@app.get("/api/compare")
def compare_goals(
    min_minute: Optional[int] = Query(0, description="Filter goals scored after this minute"),
    max_possession: Optional[float] = Query(100.0, description="Filter by maximum team possession % (Find underdog counter-attacks)")
):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        all_goals = json.load(f)
    
    filtered_results = []
    
    for goal in all_goals:
        # Filter based on minute and possession cap
        if goal["minute"] >= min_minute and goal["team_possession_pct"] <= max_possession:
            
            # 1. Existing Clutch Index Math
            clutch_index = round((goal["minute"] / 90) * (5 / goal["era_avg_goals_per_game"]), 2)
            
            # 2. NEW UNORTHODOX METRIC: Possession Defiance Index
            # Lower possession means higher defiance! base calculation on 100% minus team possession
            possession_defiance = round((100 - goal["team_possession_pct"]) / 10, 2)
            
            # 3. Overall Masterclass Rating (Combination of both)
            masterclass_rating = round((clutch_index + possession_defiance) / 2, 2)
            
            goal_analysis = goal.copy()
            goal_analysis["calculated_clutch_index"] = clutch_index
            goal_analysis["possession_defiance_score"] = possession_defiance
            goal_analysis["overall_masterclass_rating"] = masterclass_rating
            
            filtered_results.append(goal_analysis)
            
    # Sort by the new overall masterclass rating!
    filtered_results = sorted(filtered_results, key=lambda x: x["overall_masterclass_rating"], reverse=True)

   # --------------------------------------------------
    # NEW BEAUTIFUL REPORT FORMAT
    # --------------------------------------------------
    if not filtered_results:
        return PlainTextResponse("🔍 No world cup goals matched your filtering criteria.")

    # Grab the highest-rated masterclass performance from your sorted list
    top_performance = filtered_results[0]  

    report = f"""
🏆 WORLD CUP MASTERCLASS ANALYTICS REPORT 🏆
--------------------------------------------------
🕒 Goal Minute: {top_performance.get('minute')}'
📈 Era Avg Goals/Game: {top_performance.get('era_avg_goals_per_game', 'N/A')}

📊 UNIQUE METRIC BREAKDOWN:
• Clutch Index: {top_performance.get('clutch_index')} / 5.0
• Possession Defiance: {top_performance.get('possession_defiance_score')} / 10.0

🔥 OVERALL MASTERCLASS RATING: {top_performance.get('overall_masterclass_rating')} / 10.0
--------------------------------------------------
Status: Engine Online & Fully Calculated.
"""
    return PlainTextResponse(report)