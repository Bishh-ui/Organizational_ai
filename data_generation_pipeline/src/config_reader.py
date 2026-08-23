from typing import Optional

import yaml


def load_config(config_path: str = "config.yaml") -> Optional[dict]:
    """Load a YAML config file and return its contents as a dict.

    Returns None (and prints a warning) if the file is missing or invalid.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[WARN] Config file not found: {config_path}")
        return None
    except yaml.YAMLError as exc:
        print(f"[ERROR] Failed to parse YAML config {config_path}: {exc}")
        return None
