from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _find_matches(path: Path, term: str) -> list[int]:
    return [
        line_number for line_number, line in enumerate(path.read_text().splitlines(), start=1) if term in line.lower()
    ]


def test_removed_observability_provider_is_not_configured() -> None:
    removed_provider = "log" + "fire"
    checked_paths = [
        "pyproject.toml",
        ".env.sample",
        "website/settings/dev.py",
        "website/settings/prod.py",
        "blog/services/chatgpt.py",
        "core/views.py",
        "CLAUDE.md",
    ]

    offenders = {path: lines for path in checked_paths if (lines := _find_matches(ROOT / path, removed_provider))}
    assert not offenders

    lockfile = (ROOT / "uv.lock").read_text()
    assert f'name = "{removed_provider}"' not in lockfile
    assert f'extra = ["{removed_provider}"' not in lockfile
    assert f'extras = ["{removed_provider}"' not in lockfile
