import os
import json
from dotenv import load_dotenv

load_dotenv()

# Parse logic dynamically extracting values locally or strictly through runner Secrets
config_path = os.path.join(os.path.dirname(__file__), "..", "source_config.json")
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        source_config = json.load(f)
else:
    source_config_str = os.getenv("SOURCE_CONFIG_JSON")
    source_config = json.loads(source_config_str) if source_config_str else []

SOURCES = {item.get("source_name"): item for item in source_config if "source_name" in item}

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    LOCAL_DATABASE_URI = "sqlite:///local_db.sqlite3"