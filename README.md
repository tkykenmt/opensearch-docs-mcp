# opensearch-docs-mcp

[![PyPI version](https://badge.fury.io/py/opensearch-docs-mcp.svg)](https://badge.fury.io/py/opensearch-docs-mcp)
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
- 🎯 **Version Support** - Search docs for specific OpenSearch versions (default: 3.0)

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

Search OpenSearch documentation.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | (required) | Search query |
| `version` | string | "3.0" | OpenSearch version |
| `limit` | integer | 10 | Max results per page |
| `offset` | integer | 0 | Skip first N results for pagination |

**Example:**
```json
{
  "query": "k-NN",
  "version": "3.0",
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
| `version` | string | "3.0" | OpenSearch version |
| `limit` | integer | 10 | Max results per page |
| `offset` | integer | 0 | Skip first N results for pagination |

**Example:**
```json
{
  "query": "release",
  "version": "3.0",
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

## Development

```bash
# Clone and install
git clone https://github.com/tkykenmt/opensearch-docs-mcp.git
cd opensearch-docs-mcp
uv sync

# Run in development mode
uv run mcp dev src/opensearch_docs_mcp/server.py

# Run tests
uv run pytest tests/ -v
```

## License

MIT

## Disclaimer

This project uses the "OpenSearch" name to indicate compatibility with OpenSearch software. OpenSearch is a trademark of the OpenSearch Project. This tool is not affiliated with, endorsed by, or sponsored by the OpenSearch Project or its contributors.
