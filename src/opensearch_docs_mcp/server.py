"""OpenSearch Documentation MCP Server."""

import json
import urllib.parse
import urllib.request
from functools import lru_cache

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("opensearch-docs")


@lru_cache(maxsize=100)
def _fetch_docs(query: str, version: str, types: str) -> tuple:
    """Fetch docs from OpenSearch Search API (cached)."""
    encoded = urllib.parse.quote(query)
    url = f"https://search-api.opensearch.org/search?q={encoded}&v={version}&t={types}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    return tuple(data.get("results", []))


@lru_cache(maxsize=100)
def _fetch_forum(query: str) -> tuple:
    """Fetch forum posts from OpenSearch Forum API (cached)."""
    encoded = urllib.parse.quote(query)
    url = f"https://forum.opensearch.org/search/query?term={encoded}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    posts = data.get("posts", [])
    topics = {t["id"]: t for t in data.get("topics", [])}
    return tuple(posts), topics, data.get("grouped_search_result", {}).get("more_posts", False)


def _search_content(query: str, version: str, types: str, limit: int, offset: int) -> dict:
    """Internal search function for docs/blogs."""
    all_results = list(_fetch_docs(query, version, types))
    total = len(all_results)
    page_results = all_results[offset : offset + limit]

    results = []
    for r in page_results:
        url = r["url"]
        if r["type"] == "DOCS":
            url = f"https://docs.opensearch.org{url}"
        results.append({
            "title": r["title"],
            "url": url,
            "snippet": r.get("content", "")[:300],
        })

    return {
        "query": query,
        "version": version,
        "total": total,
        "offset": offset,
        "limit": limit,
        "hasMore": offset + limit < total,
        "results": results,
    }


@mcp.tool()
def search_docs(
    query: str,
    version: str = "3.0",
    limit: int = 10,
    offset: int = 0,
) -> dict:
    """Search OpenSearch documentation.

    Args:
        query: Search query
        version: OpenSearch version (default: 3.0)
        limit: Max results per page (default: 10)
        offset: Skip first N results for pagination (default: 0)
    """
    return _search_content(query, version, "docs", limit, offset)


@mcp.tool()
def search_blogs(
    query: str,
    version: str = "3.0",
    limit: int = 10,
    offset: int = 0,
) -> dict:
    """Search OpenSearch blog posts.

    Args:
        query: Search query
        version: OpenSearch version (default: 3.0)
        limit: Max results per page (default: 10)
        offset: Skip first N results for pagination (default: 0)
    """
    return _search_content(query, version, "blogs", limit, offset)


@mcp.tool()
def search_forum(query: str, limit: int = 10) -> dict:
    """Search OpenSearch community forum.

    Args:
        query: Search query
        limit: Max results (default: 10)
    """
    posts, topics, has_more = _fetch_forum(query)
    posts = list(posts)[:limit]

    results = []
    for p in posts:
        topic = topics.get(p.get("topic_id"), {})
        results.append({
            "title": topic.get("title", ""),
            "url": f"https://forum.opensearch.org/t/{topic.get('slug', '')}/{p.get('topic_id')}",
            "author": p.get("username", ""),
            "snippet": p.get("blurb", "")[:300],
            "created_at": p.get("created_at", ""),
            "tags": topic.get("tags", []),
            "has_accepted_answer": topic.get("has_accepted_answer", False),
        })

    return {
        "query": query,
        "total": len(results),
        "hasMore": has_more,
        "results": results,
    }


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
