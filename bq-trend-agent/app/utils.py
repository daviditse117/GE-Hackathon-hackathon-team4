import os
from dotenv import find_dotenv, load_dotenv
from google.cloud import bigquery
from jinja2 import Environment, FileSystemLoader

load_dotenv(find_dotenv(usecwd=True), override=True)
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-a4961fe98f0c")

def load_nl2sql_with_few_shot_prompt(refresh_date_value: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(os.path.join(current_dir, "prompts")))
    template = env.get_template("google_trends_nl2sql_with_few_shot.j2")
    return template.render(
        refresh_date_value=refresh_date_value,
        GOOGLE_CLOUD_PROJECT=os.getenv("GOOGLE_CLOUD_PROJECT", GOOGLE_CLOUD_PROJECT),
    )

def get_latest_refresh_date(
    table_name: str = "bigquery-public-data.google_trends.international_top_terms",
) -> str | None:
    try:
        client = bigquery.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT", GOOGLE_CLOUD_PROJECT))
        query = f"SELECT MAX(refresh_date) AS latest_date FROM `{table_name}`"
        for row in client.query(query).result():
            if row and row.latest_date:
                return row.latest_date.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error fetching refresh_date: {e}")
    return None
