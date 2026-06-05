from __future__ import annotations

from dataclasses import asdict
import json
from typing import Any

from .models import RepoProfile


def profile_to_dict(profile: RepoProfile) -> dict[str, Any]:
    data = asdict(profile)
    data["repo_path"] = str(profile.repo_path)
    data["generated_on"] = profile.generated_on.isoformat()
    return data


def render_json(profile: RepoProfile) -> str:
    return json.dumps(profile_to_dict(profile), ensure_ascii=False, indent=2) + "\n"
