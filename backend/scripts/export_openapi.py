"""Export the FastAPI app's OpenAPI schema to a static JSON file.

Not committed to the repo (see docs/concept.md: treated like generated
Protobuf code). Regenerated at dev/build/CI time so the frontend can run
`npm run generate:api` without needing a running backend server.

Usage (run from backend/, so "app" is importable): uv run python -m scripts.export_openapi
"""

import json
from pathlib import Path

from app.main import app

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "openapi.json"


def main() -> None:
    schema = app.openapi()
    OUTPUT_PATH.write_text(json.dumps(schema, indent=2) + "\n")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
