from fastapi import FastAPI
from fastapi.responses import PlainTextResponse  #  This is the correct path
from pydantic import BaseModel
from typing import Optional
import os
import json

app = FastAPI(title="Atlas Lions & Cross-Era World Cup Engine")

# Path to our World Cup JSON database
DATA_FILE = "data/worldcup_goals.json"

def init_database():
    """Loads World Cup historical records safely from our local JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Run database initializer
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
    # ❌ DELETE the 'with open(DATA_FILE)...' lines here
    # Just read straight from the global all_goals list!
    filtered_results = []
    
    for goal in all_goals:
        # Your filtering math loop goes here...
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
   # --------------------------------------------------
    # VISUAL HTML RESPONSE CARD
    # --------------------------------------------------
    if not filtered_results:
        return HTMLResponse("🚨 <span style='color: #ff6b6b; font-family: sans-serif;'>No historic World Cup matches matched your filter criteria.</span>")

    # Get the number one rated masterclass match
    top = filtered_results[0]

    html_content = f"""
    <html>
        <head>
            <style>
                .card {{
                    font-family: 'Segoe UI', Roboto, sans-serif;
                    background: #1a1c23;
                    color: #ffffff;
                    border-radius: 12px;
                    padding: 24px;
                    border: 1px solid #2d3139;
                    max-width: 450px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                }}
                .title {{ color: #00fff0; font-size: 20px; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #2d3139; padding-bottom: 8px; }}
                .player-header {{ font-size: 18px; color: #ffb800; margin-bottom: 10px; }}
                .stat-row {{ display: flex; justify-content: space-between; margin: 8px 0; font-size: 15px; color: #a0aec0; }}
                .stat-val {{ color: #ffffff; font-weight: bold; }}
                .rating-box {{ background: #2d3748; padding: 12px; border-radius: 8px; text-align: center; margin-top: 15px; }}
                .rating-num {{ font-size: 32px; color: #00ff66; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="title">🏆 WORLD CUP ANALYTICS ENGINE</div>
                <div class="player-header">👤 {top.get('player', 'Unknown')} ({top.get('year', 'N/A')})</div>
                
                <div class="stat-row"><span>🎯 Match Stage:</span><span class="stat-val">{top.get('stage', 'N/A')}</span></div>
                <div class="stat-row"><span>🥊 Opponent:</span><span class="stat-val">{top.get('opponent', 'N/A')}</span></div>
                <div class="stat-row"><span>🕒 Goal Minute:</span><span class="stat-val">{top.get('minute')}' min</span></div>
                <div class="stat-row"><span>📈 Era Avg Goals/Game:</span><span class="stat-val">{top.get('era_avg_goals_per_game', 'N/A')}</span></div>
                <div class="stat-row"><span>⚽ Team Possession:</span><span class="stat-val">{top.get('team_possession_pct')}%</span></div>
                
                <div class="rating-box">
                    <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #cbd5e0;">Overall Masterclass Rating</div>
                    <div class="rating-num">{top.get('overall_masterclass_rating')} / 10.0</div>
                    <div style="font-size: 13px; color: #a0aec0; margin-top: 5px;">
                        ⚡ Clutch: {top.get('calculated_clutch_index')} | 🧩 Defiance: {top.get('possession_defiance_score')}
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)