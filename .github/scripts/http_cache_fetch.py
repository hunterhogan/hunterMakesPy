#!/usr/bin/env python3
"""
HTTP fetch with ETag caching support for GitHub Actions workflows.

This script provides ETag-based conditional HTTP requests to minimize network usage
and improve workflow performance when fetching frequently-accessed resources.
"""

from pathlib import Path
from typing import Any
import json
import sys
import urllib.error
import urllib.request

# Constants
HTTP_NOT_MODIFIED = 304
MIN_ARGS_REQUIRED = 2
OUTPUT_FILE_ARG_INDEX = 2


class InvalidURLSchemeError(ValueError):
    """Raised when URL scheme is not http or https."""

    def __init__(self, url: str) -> None:
        super().__init__(f"URL '{url}' must start with 'http:' or 'https:'")


def fetch_with_etag_cache(
    url: str,
    cache_dir: str = ".http-cache",
    output_file: str | None = None
) -> dict[str, Any]:
    """
    Fetch a URL with ETag caching support.

    Parameters
    ----------
    url : str
        The URL to fetch
    cache_dir : str, optional
        Directory to store cache files (default: ".http-cache")
    output_file : str or None, optional
        Optional file to write the response data to

    Returns
    -------
    dict[str, Any]
        Dictionary containing the fetched data

    Raises
    ------
    InvalidURLSchemeError
        If URL scheme is not http or https
    urllib.error.HTTPError
        For HTTP errors other than 304
    OSError
        For file system errors
    json.JSONDecodeError
        For invalid JSON in response
    """
    # Validate URL scheme for security
    if not url.startswith(("http:", "https:")):
        raise InvalidURLSchemeError(url)

    # Set up cache directory
    cache_path = Path(cache_dir)
    cache_path.mkdir(exist_ok=True)

    # Generate cache file names based on URL
    url_hash = str(hash(url))
    etag_file = cache_path / f"etag_{url_hash}.txt"
    data_file = cache_path / f"data_{url_hash}.json"

    # Read cached ETag if available
    cached_etag = None
    if etag_file.exists():
        cached_etag = etag_file.read_text().strip()

    # Prepare request with conditional headers
    req = urllib.request.Request(url)
    if cached_etag:
        req.add_header('If-None-Match', cached_etag)

    response_data = None
    try:
        # Attempt to fetch with conditional request
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read())

            # Save new ETag and data
            new_etag = response.headers.get('ETag')
            if new_etag:
                etag_file.write_text(new_etag)

            data_file.write_text(json.dumps(response_data))

    except urllib.error.HTTPError as e:
        if e.code == HTTP_NOT_MODIFIED and data_file.exists():
            # Use cached data on 304 Not Modified
            response_data = json.loads(data_file.read_text())
        else:
            # Re-raise for other HTTP errors
            raise
    except (OSError, json.JSONDecodeError):
        # Fallback to cached data if available
        if data_file.exists():
            response_data = json.loads(data_file.read_text())
        else:
            # Last resort: fetch without conditional headers
            with urllib.request.urlopen(url) as response:
                response_data = json.loads(response.read())

    # Write to output file if specified
    if output_file:
        Path(output_file).write_text(json.dumps(response_data))

    return response_data


def main() -> None:
    """Command-line interface for the HTTP cache fetch utility."""
    if len(sys.argv) < MIN_ARGS_REQUIRED:
        sys.stderr.write("Usage: python http_cache_fetch.py <url> [output_file]\n")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[OUTPUT_FILE_ARG_INDEX] if len(sys.argv) > OUTPUT_FILE_ARG_INDEX else None

    try:
        data = fetch_with_etag_cache(url, output_file=output_file)
        if not output_file:
            # Print to stdout if no output file specified
            sys.stdout.write(json.dumps(data))
    except (InvalidURLSchemeError, urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        sys.stderr.write(f"Error fetching {url}: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
