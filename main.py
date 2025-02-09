import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import YouTubeSearchTool
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = "AIzaSyCmG2w7iSYfUKU211GPvssRYP_hdkPxmMM"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.7,
    max_output_tokens=2000,
    google_api_key=GOOGLE_API_KEY,
)

# YouTube Search Tool
youtube_tool = YouTubeSearchTool()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RoadmapRequest(BaseModel):
    skill: str
    experience: str
    time_duration: str
    purpose: str

def fetch_youtube_links(topic: str):
    """Fetches relevant YouTube links related to the given topic."""
    logger.info(f"Fetching YouTube links for topic: {topic}")
    results = youtube_tool.run(topic + " tutorial")
    return results

def generate_roadmap(skill: str, experience: str, time_duration: str, purpose: str):
    logger.info(f"Generating roadmap for skill: {skill}, experience: {experience}, duration: {time_duration}, purpose: {purpose}")
    prompt = f'''
    You are an AI mentor helping individuals develop skills.
    Generate a detailed weekly roadmap for learning {skill} for someone with {experience} experience within the duration of {time_duration} & plan it accordingly so that the student can achieve purpose {purpose}.
    Break the roadmap into weekly milestones and include:
    - Key topics to learn each week
    - Hands-on projects for each week
    - Time estimates for each week
    - Career opportunities related to the skill
    '''
    
    response = llm.invoke(prompt)
    roadmap = response.content if response else "Error generating roadmap."
    
    weekly_milestones = roadmap.split("\n\n")
    roadmap_with_links = ""
    for week in weekly_milestones:
        roadmap_with_links += week + "\n\n"
        if "week" in week.lower():  
            topic = week.split(":")[0].strip()
            youtube_links = fetch_youtube_links(topics)
            roadmap_with_links += f"### YouTube Tutorials for {topic}:\n{youtube_links}\n\n"
    
    logger.info("Roadmap generation completed successfully.")
    return roadmap_with_links

@app.post("/generate-roadmap")
def get_roadmap(request: RoadmapRequest):
    try:
        logger.info("Received request for roadmap generation.")
        roadmap = generate_roadmap(request.skill, request.experience, request.time_duration, request.purpose)
        logger.info("Successfully generated roadmap.")
        return {"roadmap": roadmap}
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
