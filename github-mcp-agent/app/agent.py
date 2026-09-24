import logging
import os

from dotenv import find_dotenv, load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

MCPToolset = McpToolset

load_dotenv(find_dotenv(usecwd=True), override=True)
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-a4961fe98f0c")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

logger = logging.getLogger(__name__)
GITHUB_MCP_ENDPOINT = "https://api.githubcopilot.com/mcp/"


def create_github_mcp_toolset() -> MCPToolset:
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "").strip()
    if not github_token or github_token == "YOUR_GITHUB_ACCESS_TOKEN_HERE":
        logger.warning("Set a valid GITHUB_PERSONAL_ACCESS_TOKEN in app/.env!")

    connection_params = StreamableHTTPConnectionParams(
        url=GITHUB_MCP_ENDPOINT,
        headers={
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
        },
    )

    return MCPToolset(
        connection_params=connection_params,
        tool_filter=[
            "search_repositories",
            "search_issues",
            "list_issues",
            "get_issue",
            "create_issue",
            "get_file_contents",
        ],
    )


AGENT_LDAP = os.getenv("USER_LDAP", "dibarra")
mcp_tools = create_github_mcp_toolset()

root_agent = Agent(
    name=f"github_mcp_agent_{AGENT_LDAP}",
    model=os.getenv("GEMINI_MODEL", os.getenv("MODEL_NAME", "gemini-2.5-flash")),
    description="ADK agent that searches GitHub repositories, issues, and code via Model Context Protocol (MCP).",
    instruction=(
        "You are an expert GitHub Engineering Assistant connected directly to the "
        "GitHub Copilot MCP Server.\n"
        "- Use `search_repositories` to find repositories.\n"
        "- Use `search_issues`, `list_issues`, and `get_issue` to inspect and summarize issues.\n"
        "- Format all repository names and issue numbers as clickable Markdown links."
    ),
    tools=[mcp_tools],
)

app = App(root_agent=root_agent, name="app")
