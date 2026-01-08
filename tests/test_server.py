"""Tests for opensearch-docs-mcp."""

import json

import pytest


class TestSearchDocs:
    """Tests for search_docs tool."""

    def test_search_docs_returns_expected_structure(self):
        """Test that search_docs returns correct response structure."""
        from opensearch_docs_mcp.server import search_docs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_docs("test", limit=2)

        assert "query" in result
        assert "version" in result
        assert "total" in result
        assert "offset" in result
        assert "limit" in result
        assert "hasMore" in result
        assert "results" in result
        assert isinstance(result["results"], list)

    def test_search_docs_result_item_structure(self):
        """Test that each result item has expected fields."""
        from opensearch_docs_mcp.server import search_docs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_docs("opensearch", limit=1)

        if result["results"]:
            item = result["results"][0]
            assert "title" in item
            assert "url" in item
            assert "snippet" in item

    def test_search_docs_pagination(self):
        """Test pagination with offset."""
        from opensearch_docs_mcp.server import search_docs, _fetch_docs
        _fetch_docs.cache_clear()

        result1 = search_docs("index", limit=2, offset=0)
        result2 = search_docs("index", limit=2, offset=2)

        if result1["results"] and result2["results"]:
            assert result1["results"][0]["url"] != result2["results"][0]["url"]

    def test_search_docs_snippet_length(self):
        """Test that snippets are truncated to 300 chars."""
        from opensearch_docs_mcp.server import search_docs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_docs("configuration", limit=5)

        for item in result["results"]:
            assert len(item["snippet"]) <= 300

    def test_search_docs_url_prefix(self):
        """Test that docs URLs have correct prefix."""
        from opensearch_docs_mcp.server import search_docs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_docs("install", limit=5)

        for item in result["results"]:
            assert item["url"].startswith("https://docs.opensearch.org")


class TestSearchBlogs:
    """Tests for search_blogs tool."""

    def test_search_blogs_returns_expected_structure(self):
        """Test that search_blogs returns correct response structure."""
        from opensearch_docs_mcp.server import search_blogs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_blogs("release", limit=2)

        assert "query" in result
        assert "version" in result
        assert "total" in result
        assert "results" in result

    def test_search_blogs_result_item_structure(self):
        """Test that each blog result has expected fields."""
        from opensearch_docs_mcp.server import search_blogs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_blogs("announcement", limit=1)

        if result["results"]:
            item = result["results"][0]
            assert "title" in item
            assert "url" in item
            assert "snippet" in item


class TestSearchForum:
    """Tests for search_forum tool."""

    def test_search_forum_returns_expected_structure(self):
        """Test that search_forum returns correct response structure."""
        from opensearch_docs_mcp.server import search_forum, _fetch_forum
        _fetch_forum.cache_clear()

        result = search_forum("error", limit=2)

        assert "query" in result
        assert "total" in result
        assert "hasMore" in result
        assert "results" in result
        assert isinstance(result["results"], list)

    def test_search_forum_result_item_structure(self):
        """Test that each forum result has expected fields."""
        from opensearch_docs_mcp.server import search_forum, _fetch_forum
        _fetch_forum.cache_clear()

        result = search_forum("help", limit=1)

        if result["results"]:
            item = result["results"][0]
            assert "title" in item
            assert "url" in item
            assert "author" in item
            assert "snippet" in item
            assert "created_at" in item
            assert "tags" in item
            assert "has_accepted_answer" in item

    def test_search_forum_url_format(self):
        """Test that forum URLs have correct format."""
        from opensearch_docs_mcp.server import search_forum, _fetch_forum
        _fetch_forum.cache_clear()

        result = search_forum("setup", limit=3)

        for item in result["results"]:
            assert item["url"].startswith("https://forum.opensearch.org/t/")


class TestCache:
    """Tests for LRU cache behavior."""

    def test_cache_hit(self):
        """Test that cache returns same result on second call."""
        from opensearch_docs_mcp.server import _fetch_docs
        _fetch_docs.cache_clear()

        result1 = _fetch_docs("cache_test", "3.0", "docs")
        result2 = _fetch_docs("cache_test", "3.0", "docs")

        assert result1 == result2
        assert _fetch_docs.cache_info().hits == 1

    def test_cache_miss_different_params(self):
        """Test that different params cause cache miss."""
        from opensearch_docs_mcp.server import _fetch_docs
        _fetch_docs.cache_clear()

        _fetch_docs("test1", "3.0", "docs")
        _fetch_docs("test2", "3.0", "docs")

        assert _fetch_docs.cache_info().misses == 2

    def test_cache_maxsize(self):
        """Test that cache respects maxsize=100."""
        from opensearch_docs_mcp.server import _fetch_docs

        assert _fetch_docs.cache_info().maxsize == 100


class TestResponseSize:
    """Tests for response size (context consumption)."""

    def test_docs_response_size_reasonable(self):
        """Test that docs response doesn't exceed reasonable size."""
        from opensearch_docs_mcp.server import search_docs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_docs("vector", limit=10)
        response_json = json.dumps(result)

        assert len(response_json) < 10000, f"Response too large: {len(response_json)} chars"

    def test_blogs_response_size_reasonable(self):
        """Test that blogs response doesn't exceed reasonable size."""
        from opensearch_docs_mcp.server import search_blogs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_blogs("release", limit=10)
        response_json = json.dumps(result)

        assert len(response_json) < 10000, f"Response too large: {len(response_json)} chars"

    def test_forum_response_size_reasonable(self):
        """Test that forum response doesn't exceed reasonable size."""
        from opensearch_docs_mcp.server import search_forum, _fetch_forum
        _fetch_forum.cache_clear()

        result = search_forum("error", limit=10)
        response_json = json.dumps(result)

        assert len(response_json) < 10000, f"Response too large: {len(response_json)} chars"


class TestErrorHandling:
    """Tests for error handling."""

    def test_empty_query_results(self):
        """Test handling of query with no results."""
        from opensearch_docs_mcp.server import search_docs, _fetch_docs
        _fetch_docs.cache_clear()

        result = search_docs("xyznonexistentquery12345", limit=10)

        assert result["total"] == 0
        assert result["results"] == []
        assert result["hasMore"] is False
