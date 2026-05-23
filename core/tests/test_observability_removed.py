from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_removed_observability_provider_is_not_configured() -> None:
    removed_provider = "log" + "fire"
    checked_paths = [
        "pyproject.toml",
        ".env.sample",
        "website/settings/dev.py",
        "website/settings/prod.py",
        "blog/services/chatgpt.py",
        "core/views.py",
        "django_fast/services/cache/cache_service.py",
        "CLAUDE.md",
    ]

    offenders = {
        path: [
            line_number
            for line_number, line in enumerate((ROOT / path).read_text().splitlines(), start=1)
            if removed_provider in line.lower()
        ]
        for path in checked_paths
    }
    assert not {path: lines for path, lines in offenders.items() if lines}

    lockfile = (ROOT / "uv.lock").read_text()
    assert f'name = "{removed_provider}"' not in lockfile
    assert f'extra = ["{removed_provider}"' not in lockfile
    assert f'extras = ["{removed_provider}"' not in lockfile
