#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
SOURCE_DIR="${REPO_ROOT}/adapters/codex/plugin/workovercv"
TARGET_DIR="${HOME}/plugins/workovercv"
MARKETPLACE_DIR="${HOME}/.agents/plugins"
MARKETPLACE_PATH="${MARKETPLACE_DIR}/marketplace.json"

mkdir -p "${TARGET_DIR}"
cp -R "${SOURCE_DIR}/." "${TARGET_DIR}/"

mkdir -p "${MARKETPLACE_DIR}"
python3 - "${MARKETPLACE_PATH}" <<'PY'
import json
import sys
from pathlib import Path

marketplace_path = Path(sys.argv[1])
if marketplace_path.exists():
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
else:
    marketplace = {
        "name": "personal",
        "interface": {"displayName": "Personal"},
        "plugins": [],
    }

marketplace.setdefault("plugins", [])
marketplace["plugins"] = [
    plugin for plugin in marketplace["plugins"]
    if plugin.get("name") != "workovercv"
]
marketplace["plugins"].append({
    "name": "workovercv",
    "source": {
        "source": "local",
        "path": "./plugins/workovercv",
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    },
    "category": "Productivity",
})

marketplace_path.write_text(
    json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
PY

MARKETPLACE_NAME="$(python3 - "${MARKETPLACE_PATH}" <<'PY'
import json
import sys
from pathlib import Path

marketplace = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(marketplace["name"])
PY
)"

echo "Installed WorkOverCV plugin source to ${TARGET_DIR}"
echo "Updated personal marketplace at ${MARKETPLACE_PATH}"
echo "Run: codex plugin add workovercv@${MARKETPLACE_NAME}"
