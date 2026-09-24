# 🧟 Z-COM: Global Zombie Outbreak & Anomaly Early-Warning Command
### 🏆 Gemini Enterprise Hackathon — Team `hackathon-team4`

- **GCP Project ID**: `qwiklabs-gcp-00-a4961fe98f0c`
- **Gemini Enterprise App**: `gemini-enterprise-app-hackathon-team4`
- **Model Armor Security Policy**: `ge-security-policy-hackathon-team4`

## 🎯 Use Case Overview
Before hospitals or satellites detect **Patient Zero** of a Zombie Outbreak (or an enterprise crisis), citizens Google their bizarre symptoms and local anomalies. **Z-COM** unites **BigQuery Google Trends**, **Google Search**, and **GitHub MCP** on **Gemini Enterprise**:

1. **`bq-trend-agent/` (Z-COM Patient-Zero Epidemiologist)**:
   - Uses `BigQueryToolset(write_mode=WriteMode.BLOCKED)`, dynamic partition lookup (`utils.get_latest_refresh_date()`), and Jinja2 (`load_nl2sql_with_few_shot_prompt()`) enforcing `WHERE refresh_date = '{{ refresh_date_value }}'`, `ARRAY_AGG`, and `LIMIT 100`.
2. **`basic-search-agent/` (Z-COM Field Recon & Evacuation Scout)**:
   - Uses `google_search` from `google.adk.tools` (`App(root_agent=...)`) to verify live breaking events and classify Zombie Threat Levels (`LEVEL 0` to `DEFCON-1`).
3. **`github-mcp-agent/` (Z-COM Bunker Quartermaster & DevOps Dispatcher)**:
   - Connects `MCPToolset` (`StreamableHTTPConnectionParams`) to `https://api.githubcopilot.com/mcp/` via `Authorization: Bearer <GITHUB_PERSONAL_ACCESS_TOKEN>` to search repos/issues and file `[Z-COM DEFCON-1]` Containment Tickets (`create_issue`).
4. **`extension-trendops-agent/` (20-Point Extension — Autonomous Apocalypse Defense Grid)**:
   - Multi-Agent ADK Coordinator (`sub_agents=[bq_trends_subagent, search_subagent, github_mcp_subagent]`) guarded by **Gemini Enterprise Model Armor** (`INSPECT_AND_BLOCK` for PII & Prompt Injection).

## 🚀 Setup, Local Testing & Deployment
1. Set project: `gcloud config set project qwiklabs-gcp-00-a4961fe98f0c`
2. Copy `.env.example` to `.env` in each agent's `app/` directory and add `GITHUB_PERSONAL_ACCESS_TOKEN`.
3. Run locally: `uv sync && uv run adk web . --port 8501 --reload_agents --allow_origins "*"`
4. Deploy & Register: `make backend && make register-gemini-enterprise`
