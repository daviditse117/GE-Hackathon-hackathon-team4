import os
from google.adk.agents import Agent
from google.adk.apps.app import App
from basic_search_agent.app.agent import root_agent as search_subagent
from bq_trend_agent.app.agent import root_agent as bq_trends_subagent
from github_mcp_agent.app.agent import root_agent as github_mcp_subagent

AGENT_LDAP = os.getenv("USER_LDAP", "dibarra")

root_agent = Agent(
    name=f"trendops_coordinator_{AGENT_LDAP}",
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    description="Autonomous TrendOps Multi-Agent Orchestrator uniting BQ Trends, Google Search, and GitHub MCP.",
    instruction=(
        "Coordinate `bq_trend_agent`, `basic_search_agent`, and `github_mcp_agent` to detect "
        "breakout search spikes in BigQuery, verify live news context via Google Search, and "
        "search/create engineering tracking issues in GitHub via MCP."
    ),
    sub_agents=[bq_trends_subagent, search_subagent, github_mcp_subagent],
)

app = App(root_agent=root_agent, name="app")
