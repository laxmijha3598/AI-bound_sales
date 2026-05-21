from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    load_dotenv_file()
    with Path(path).open("rb") as f:
        config = tomllib.load(f)

    campaign = config.setdefault("campaign", {})
    campaign["calendly_link"] = os.getenv("CALENDLY_LINK") or campaign.get("calendly_link", "")
    return config


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def load_dotenv_file(path: str | Path = ".env") -> None:
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
