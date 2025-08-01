from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from google.api_core import retry
import os
from dotenv import load_dotenv
import time
from app.mock_data import get_mock_data
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://langtrack-project-assistant.vercel.app",],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
# Load mock data
mock_data = get_mock_data()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class Query(BaseModel):
    question: str

def format_for_display(data: Dict[str, Any]) -> str:
    """Format the mock data into human-readable text with team info"""
    projects = []
    for p in data['projects']:
        # Get team member names
        members = []
        for member_id in p['team']:
            member = next((m for m in data['team'] if m['id'] == member_id), None)
            if member:
                members.append(member['name'])
        
        project_text = f"""
        - {p['name']} (ID: {p['id']})
          Status: {p['status']}
          Progress: {p['progress']}%
          Timeline: {p['start_date']} to {p['deadline']}
          Team: {', '.join(members) if members else 'Not assigned'}
        """
        projects.append(project_text)
    
    return f"""
    Here is the current project information:
    
    {''.join(projects)}
    """

def build_prompt(question: str) -> str:
    context = format_for_display(mock_data)
    
    return f"""
    You are a helpful project management assistant. Use this project data to answer questions:
    
    {context}
    
    Current Team Members:
    {format_team_list(mock_data['team'])}
    
    Please answer the following question naturally:
    Question: "{question}"
    
    Important Response Rules:
    1. ALWAYS use real names instead of IDs
    2. For team questions, list all members working on a project
    3. Be concise but friendly
    4. If a project has no team assigned, say "No team assigned yet"
    """
    
def format_team_list(team):
    return "\n".join(f"- {m['name']} ({m['role']})" for m in team)

@retry.Retry(
    initial=1.0,
    maximum=60.0,
    multiplier=2.0,
    deadline=300.0
)
def generate_with_retry(prompt: str):
    try:
        # Correct Gemini API request format
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(10)
        raise

@app.post("/ask")
async def ask_question(query: Query) -> Dict[str, Any]:
    try:
        full_prompt = build_prompt(query.question)
        response = generate_with_retry(full_prompt)
        
        return {
            "success": True,
            "data": {
                "question": query.question,
                "answer": response.strip(),
                "projects": mock_data['projects'],  # Include raw data if needed
                "formatted": True,  # Indicates markdown formatting
                "timestamp": int(time.time())
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "message": str(e),
                "code": "GEMINI_API_ERROR" if "gemini" in str(e).lower() else "SERVER_ERROR"
            },
            "timestamp": int(time.time())
        }

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)