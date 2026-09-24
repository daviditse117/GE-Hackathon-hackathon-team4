import logging
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools import google_search
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler

load_dotenv()

os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-a4961fe98f0c")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")

try:
    client = google.cloud.logging.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])
    handler = CloudLoggingHandler(client)
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(handler)
    logging.info("Cloud Logging initialized for ADK agent script")
    handler.close()
except Exception as e:
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Cloud Logging fallback to standard logger: {e}")

AGENT_LDAP = os.getenv("USER_LDAP", "dibarra")

root_agent = Agent(
    name=f"basic_search_agent_{AGENT_LDAP}",
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    description="Agent to answer questions using Google Search.",
    instruction="I can answer your questions by searching the internet. You are Z-COM Recon-1! Use google_search to answer accurately, then add a fun 🧟 Z-COM Zombie Threat Level (Level 0 to DEFCON-1) and bunker evacuation tip!",
    tools=[google_search],
)

app = App(root_agent=root_agent, name="app")
