from fastapi import FastAPI, Query
from typing import Optional
import json
import os

app = FastAPI(title="Atlas Lions & Cross-Era World Cup Engine")

# Path to our JSON dataset inside the container
DATA_FILE = "data/worldcup_goals.json"

def init_database():
    """Safely loads World Cup historical records on startup."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Load the data once when the server boots up
all_goals = init_database()

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
    max_possession: Optional[float] = Query(100.0, description="Filter by maximum team possession")
):
    filtered_results = []
    
    for goal in all_goals:
        if goal["minute"] >= min_minute and goal["team_possession_pct"] <= max_possession:
            # Calculate metrics
            clutch_index = round((goal["minute"] / 90) * (5 / goal["era_avg_goals_per_game"]), 2)
            possession_defiance = round((100 - goal["team_possession_pct"]) / 10, 2)
            overall_masterclass = round((clutch_index + possession_defiance) / 2, 2)
            
            # Build the clean response record
            enhanced_goal = goal.copy()
            enhanced_goal["calculated_clutch_index"] = clutch_index
            enhanced_goal["possession_defiance_score"] = possession_defiance
            enhanced_goal["overall_masterclass_rating"] = overall_masterclass
            
            filtered_results.append(enhanced_goal)
            
    return {
        "filters_applied": {
            "min_minute": min_minute,
            "max_possession_allowed": max_possession
        },
        "total_matches_found": len(filtered_results),
        "comparison_matrix": filtered_results
    }