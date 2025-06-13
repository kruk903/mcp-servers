#!/bin/bash
# Create a tar.gz package of the MCP servers for Claude Desktop
# Usage: ./scripts/package_for_claude.sh [output_file]
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT=${1:-claude-mcp-servers.tar.gz}
cd "$ROOT_DIR"
# Exclude git metadata and existing archive
tar --exclude=.git --exclude="$OUTPUT" -czf "$OUTPUT" .
echo "Package created: $OUTPUT"

