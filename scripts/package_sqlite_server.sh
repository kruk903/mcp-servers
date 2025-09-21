#!/bin/bash
# Create a tar.gz package containing only the SQLite MCP server.
# Usage: ./scripts/package_sqlite_server.sh [output_file]
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT=${1:-claude-sqlite-server.tar.gz}
cd "$ROOT_DIR"
# Exclude git metadata and any existing output archive
files=(
    LICENSE
    README.md
    src/sqlite
)
tar --exclude=.git --exclude="$OUTPUT" -czf "$OUTPUT" "${files[@]}"
echo "Package created: $OUTPUT"

