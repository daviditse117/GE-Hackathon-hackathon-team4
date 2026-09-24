import datetime
import os
from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
import google.auth
from .utils import get_latest_refresh_date, load_nl2sql_with_few_shot_prompt

load_dotenv(find_dotenv(usecwd=True), override=True)
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-a4961fe98f0c")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")

credentials, _ = google.auth.default()
bigquery_toolset = BigQueryToolset(
    credentials_config=BigQueryCredentialsConfig(credentials=credentials),
    bigquery_tool_config=BigQueryToolConfig(write_mode=WriteMode.BLOCKED),
)

latest_refresh_date = get_latest_refresh_date() or (
    datetime.date.today() - datetime.timedelta(days=1)
).strftime("%Y-%m-%d")

root_agent = Agent(
    name="bq_trend_agent",
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    description="Z-COM BigQuery SQL Epidemiologist for Google Trends.",
    instruction=load_nl2sql_with_few_shot_prompt(refresh_date_value=latest_refresh_date),
    tools=[bigquery_toolset],
)

app = App(root_agent=root_agent, name="app")
