# 🏆 GE Hackathon Project — Team `hackathon-team4`

- **GCP Project ID**: `qwiklabs-gcp-00-a4961fe98f0c`
- **Gemini Enterprise App**: `gemini-enterprise-app-hackathon-team4`
- **Model Armor Security Policy**: `ge-security-policy-hackathon-team4`

## Overview
This repository contains Team `hackathon-team4`'s completed Google ADK (Agent Development Kit) agents, Gemini Enterprise + Model Armor configuration manifest (`ge-config/ge_app_manifest.json`), and our **TrendOps Multi-Agent Extension** (`extension-trendops-agent/`) for the Gemini Enterprise Hackathon.

## Repository Contents
- `ge-config/ge_app_manifest.json`: Exported Gemini Enterprise App configuration manifest and Model Armor policy metadata (`INSPECT_AND_BLOCK` for Credit Card, US SSN, Email PII, Prompt Injection, and Malicious URLs).
- `basic-search-agent/`: Basic search ADK agent (`App(root_agent=...)`) integrated with `google_search` from `google.adk.tools` and Cloud Logging.
- `bq-trend-agent/`: BigQuery SQL analyst agent using `BigQueryToolset(write_mode=WriteMode.BLOCKED)`, dynamic partition lookup (`utils.get_latest_refresh_date()`), and Jinja2 prompt rendering (`load_nl2sql_with_few_shot_prompt()`) enforcing `refresh_date` filtering, `ARRAY_AGG`, and `LIMIT 100`.
- `github-mcp-agent/`: ADK agent leveraging Model Context Protocol (`MCPToolset` + `StreamableHTTPConnectionParams`) to query `https://api.githubcopilot.com/mcp/` securely via environment-injected `Bearer <GITHUB_PERSONAL_ACCESS_TOKEN>`.
- `extension-trendops-agent/`: Multi-agent coordinator uniting all three agents into an autonomous Market-to-GitHub workflow.

## Setup Instructions
1. Clone this repository and `cd` into any agent folder (`basic-search-agent`, `bq-trend-agent`, or `github-mcp-agent`).
2. Copy `app/.env.example` to `app/.env` and fill in `GITHUB_PERSONAL_ACCESS_TOKEN` for the GitHub MCP agent.
3. Install dependencies and launch ADK Web Playground:
   ```bash
   uv sync && uv run adk web . --port 8501 --reload_agents --allow_origins "*"
   ```
4. Deploy to Vertex AI Agent Engine & Register with Gemini Enterprise:
   ```bash
   make backend
   make register-gemini-enterprise
   ```
