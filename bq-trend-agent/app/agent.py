import datetime
import logging
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

logger = logging.getLogger(__name__)


def create_bigquery_toolset() -> BigQueryToolset:
    try:
        credentials, _ = google.auth.default()
        credentials_config = BigQueryCredentialsConfig(credentials=credentials)
        tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)
        return BigQueryToolset(
            credentials_config=credentials_config,
            bigquery_tool_config=tool_config,
        )
    except Exception as e:
        logger.error(f"Failed to initialize BigQueryToolset: {e}")
        raise


def build_agent_instruction() -> str:
    latest_refresh_date = get_latest_refresh_date()
    if not latest_refresh_date:
        latest_refresh_date = (
            datetime.date.today() - datetime.timedelta(days=1)
        ).strftime("%Y-%m-%d")
    return load_nl2sql_with_few_shot_prompt(refresh_date_value=latest_refresh_date)


AGENT_LDAP = os.getenv("USER_LDAP", "dibarra")
bigquery_toolset = create_bigquery_toolset()
system_instruction = build_agent_instruction()

root_agent = Agent(
    name=f"bq_trend_agent_{AGENT_LDAP}",
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    description=(
        "BigQuery SQL expert agent designed to answer natural language questions about "
        "top trending and rising international search terms from Google Trends."
    ),
    instruction=system_instruction,
    tools=[bigquery_toolset],
)

app = App(root_agent=root_agent, name="app")
