import datetime
import os
from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
import google.auth
from .utils import get_latest_refresh_date, load_nl2sql_with_few_shot_prompt

MCPToolset = McpToolset
load_dotenv(find_dotenv(usecwd=True), override=True)
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-a4961fe98f0c")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")

credentials, _ = google.auth.default()
bigquery_toolset = BigQueryToolset(
    credentials_config=BigQueryCredentialsConfig(credentials=credentials),
    bigquery_tool_config=BigQueryToolConfig(write_mode=WriteMode.BLOCKED),
)

github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "").strip()
mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
        },
    ),
    tool_filter=[
        "search_repositories",
        "search_issues",
        "list_issues",
        "get_issue",
        "create_issue",
        "get_file_contents",
    ],
)

latest_refresh_date = get_latest_refresh_date() or (
    datetime.date.today() - datetime.timedelta(days=1)
).strftime("%Y-%m-%d")

bq_prompt = load_nl2sql_with_few_shot_prompt(refresh_date_value=latest_refresh_date)
unified_instruction = (
    bq_prompt
    + "\n\n### 5. Z-COM Quartermaster (GitHub MCP Capabilities)\n"
    + "You ALSO have direct access to GitHub via MCP (`search_repositories`, `search_issues`, "
    + "`list_issues`, `get_issue`, `create_issue`, `get_file_contents`).\n"
    + "- When asked to search GitHub repositories or issues (e.g. `google/adk-python`), ALWAYS use "
    + "`search_issues`, `list_issues`, or `search_repositories` and format results with clickable links.\n"
    + "- When asked to create a Z-COM Quarantine Ticket in `daviditse117/GE-Hackathon-hackathon-team4`, "
    + "use `create_issue`!"
)

root_agent = Agent(
    name="zcom_bq_agent",
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    description="Unified Z-COM Epidemiologist (BigQuery Trends) & Bunker Quartermaster (GitHub MCP).",
    instruction=unified_instruction,
    tools=[bigquery_toolset, mcp_tools],
)

app = App(root_agent=root_agent, name="app")
