# Packaging MCP Servers for Claude Desktop

This repository contains multiple Model Context Protocol (MCP) servers under the `src/` directory. Each server can be used by tools like Claude Desktop to provide additional capabilities.

The script `scripts/package_for_claude.sh` creates a `tar.gz` archive with all repository files (excluding Git metadata). You can run it from the repository root:

```bash
./scripts/package_for_claude.sh
```

The resulting `claude-mcp-servers.tar.gz` contains the full file structure shown in `docs/claude_package_files.txt`.

After extracting the archive, configure Claude Desktop by adding entries in `claude_desktop_config.json`. For example, to run the memory server:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

Additional examples are available in the project [README](../README.md).

## Packaging only the SQLite server

If you just need a database server that Claude can create tables and run queries against, use the `package_sqlite_server.sh` script:

```bash
./scripts/package_sqlite_server.sh
```

This produces `claude-sqlite-server.tar.gz` which contains the files listed in `docs/sqlite_package_files.txt`.

Add the SQLite server to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/src/sqlite",
        "run",
        "mcp-server-sqlite",
        "--db-path",
        "~/test.db"
      ]
    }
  }
}
```
