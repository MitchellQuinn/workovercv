#!/usr/bin/env bash
set -euo pipefail

mkdir -p .claude/skills/workovercv
cp -R skills/workovercv/* .claude/skills/workovercv/

echo "Installed WorkOverCV skill to .claude/skills/workovercv"
