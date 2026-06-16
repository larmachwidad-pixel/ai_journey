from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse  
from typing import Optional
import json
import os

# Updated to a global title without special characters to keep the deployment safe
app = FastAPI(title="Cross-Era World Cup Statistics Engine")

# Path to your JSON dataset inside the container
DATA_FILE = "data/worldcup_goals.json"

def init_database():
    """Safely loads World Cup historical records on startup."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Load the data once when the server boots up
all_goals = init_database()

# The root endpoint that keeps the container awake
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>World Cup API</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding-top: 50px; 
                    background-color: #f4f4f9;
                    color: #333;
                }
                .container {
                    background: white;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                h1 { color: #2c3e50; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏆 Global World Cup Statistics Engine</h1>
                <p>The container is successfully awake and running!</p>
                <p>Append <code>/docs</code> to the URL to view the interactive API documentation.</p>
            </div>
        </body>
    </html>
    """