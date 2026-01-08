# opensearch-docs-mcp

MCP server for searching OpenSearch documentation, blogs, and community forums.

> **Note**: This is an unofficial community tool and is not affiliated with or endorsed by the OpenSearch Project.

## Installation

```bash
# Using uvx (recommended)
uvx opensearch-docs-mcp

# Using pip
pip install opensearch-docs-mcp
opensearch-docs-mcp
```

## Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "opensearch-docs": {
      "command": "uvx",
      "args": ["opensearch-docs-mcp"]
    }
  }
}
```

### Cursor

Add to MCP settings:

```json
{
  "mcpServers": {
    "opensearch-docs": {
      "command": "uvx",
      "args": ["opensearch-docs-mcp"]
    }
  }
}
```

## Tools

### search_docs

Search OpenSearch documentation and blogs.

Parameters:
- `query` (required): Search query
- `version`: OpenSearch version (default: "3.0")
- `types`: Content types - "docs", "blogs", or "docs,blogs" (default: "docs,blogs")
- `limit`: Max results per page (default: 10)
- `offset`: Skip first N results for pagination (default: 0)

### search_forum

Search OpenSearch community forum.

Parameters:
- `query` (required): Search query
- `limit`: Max results (default: 10)

## Development

```bash
# Clone and install
git clone https://github.com/yourname/opensearch-docs-mcp.git
cd opensearch-docs-mcp
uv sync

# Run in development mode
uv run mcp dev src/opensearch_docs_mcp/server.py
```

## License

MIT

## Disclaimer

This project uses the "OpenSearch" name to indicate compatibility with OpenSearch software. OpenSearch is a trademark of the OpenSearch Project. This tool is not affiliated with, endorsed by, or sponsored by the OpenSearch Project or its contributors.
