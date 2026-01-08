# opensearch-docs-mcp

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP server for searching OpenSearch documentation, blogs, and community forums.

> **Note**: This is an unofficial community tool and is not affiliated with or endorsed by the OpenSearch Project.

## Features

- 🔍 **Documentation Search** - Search official OpenSearch docs
- 📝 **Blog Search** - Search OpenSearch blog posts
- 💬 **Forum Search** - Search community forum posts and discussions
- 🚀 **Fast** - LRU cache (100 entries) for repeated queries
- 📦 **Zero Config** - Works out of the box with Claude Desktop, Cursor, etc.
- 🎯 **Version Support** - Search docs for specific OpenSearch versions (default: latest)

## Installation

```bash
git clone https://github.com/tkykenmt/opensearch-docs-mcp.git
cd opensearch-docs-mcp
uv sync
```

## Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "opensearch-docs": {
      "command": "uv",
      "args": ["--directory", "/path/to/opensearch-docs-mcp", "run", "opensearch-docs-mcp"]
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
      "command": "uv",
      "args": ["--directory", "/path/to/opensearch-docs-mcp", "run", "opensearch-docs-mcp"]
    }
  }
}
```

## Tools

### search_docs

Search OpenSearch documentation.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | (required) | Search query |
| `version` | string | "latest" | OpenSearch version (e.g., "2.17", "3.0") |
| `limit` | integer | 10 | Max results per page |
| `offset` | integer | 0 | Skip first N results for pagination |

**Example:**
```json
{
  "query": "k-NN",
  "version": "latest",
  "total": 18,
  "hasMore": true,
  "results": [
    {
      "title": "k-NN",
      "url": "https://docs.opensearch.org/3.0/query-dsl/specialized/k-nn/index/",
      "snippet": "Use the knn query for running nearest neighbor searches on vector fields."
    }
  ]
}
```

### search_blogs

Search OpenSearch blog posts.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | (required) | Search query |
| `version` | string | "latest" | OpenSearch version (e.g., "2.17", "3.0") |
| `limit` | integer | 10 | Max results per page |
| `offset` | integer | 0 | Skip first N results for pagination |

**Example:**
```json
{
  "query": "release",
  "version": "latest",
  "total": 5,
  "hasMore": false,
  "results": [
    {
      "title": "OpenSearch 3.0 is here!",
      "url": "https://opensearch.org/blog/opensearch-3-0-is-here/",
      "snippet": "We are excited to announce the release of OpenSearch 3.0..."
    }
  ]
}
```

### search_forum

Search OpenSearch community forum.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | (required) | Search query |
| `limit` | integer | 10 | Max results |

**Example:**
```json
{
  "query": "vector search",
  "total": 5,
  "hasMore": true,
  "results": [
    {
      "title": "Why my OpenSearch vector search is slow",
      "url": "https://forum.opensearch.org/t/why-my-opensearch-vector-search-is-slow/16166",
      "author": "Garance",
      "snippet": "I'm experiencing slow vector search performance...",
      "created_at": "2023-10-05T17:10:42.440Z",
      "tags": [],
      "has_accepted_answer": false
    }
  ]
}
```

## Combining with Other MCPs

This MCP focuses on OpenSearch knowledge resources (docs, blogs, forum). For source code search, use it together with the [GitHub MCP](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github):

> **Note**: The original MCP GitHub server has been archived. The official [GitHub MCP Server](https://github.com/github/github-mcp-server) requires a GitHub PAT, so we use the archived version with `gh auth token` as a workaround.

| Use Case | MCP |
|----------|-----|
| API usage, configuration, concepts | OpenSearch Docs MCP |
| Implementation details, source code | GitHub MCP |

Example workflow:
1. Search docs/blogs for "semantic field" usage → OpenSearch Docs MCP
2. Find the actual implementation in `opensearch-project/OpenSearch` → GitHub MCP

### Using GitHub MCP with Kiro CLI

If you're using Kiro CLI with `gh auth token` for authentication, the GitHub MCP requires a slightly different setup since it expects a `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable.

Here's a workaround configuration:

```json
{
  "mcpServers": {
    "github": {
      "command": "sh",
      "args": ["-c", "GITHUB_PERSONAL_ACCESS_TOKEN=$(gh auth token) npx -y @modelcontextprotocol/server-github"]
    }
  }
}
```

This dynamically injects the token from `gh auth token` into the environment variable that the GitHub MCP expects.

## Development

```bash
# Run in development mode
uv run mcp dev src/opensearch_docs_mcp/server.py

# Run tests
uv run pytest tests/ -v
```

## License

MIT

## Disclaimer

This project uses the "OpenSearch" name to indicate compatibility with OpenSearch software. OpenSearch is a trademark of the OpenSearch Project. This tool is not affiliated with, endorsed by, or sponsored by the OpenSearch Project or its contributors.
