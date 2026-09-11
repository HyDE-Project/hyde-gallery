#!/usr/bin/env python3
"""
Script to check if all links in hyde-themes.json are accessible.
Outputs broken links as JSON to stdout for the workflow to use.
"""

import json
import sys
import urllib.request
import urllib.error
import socket

TIMEOUT = 10
JSON_FILE = "hyde-themes.json"


def check_link(url: str) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "HyDE-Gallery-LinkChecker/1.0 (GitHub Actions)"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            if 200 <= response.status < 400:
                return True, ""
            return False, f"HTTP {response.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"URL Error: {e.reason}"
    except socket.timeout:
        return False, "Timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        themes = json.load(f)

    broken_links = []
    total_links = 0

    for theme in themes:
        theme_name = theme.get("THEME", "Unknown")
        link = theme.get("LINK", "")

        if not link:
            continue

        total_links += 1
        is_accessible, error = check_link(link)

        if not is_accessible:
            broken_links.append({
                "theme": theme_name,
                "link": link,
                "error": error,
            })
            print(f"❌ Broken: {theme_name} - {link} ({error})")
        else:
            print(f"✅ OK: {theme_name} - {link}")

    # Output broken links as JSON for workflow to consume
    result = {
        "has_broken": len(broken_links) > 0,
        "total": total_links,
        "broken_count": len(broken_links),
        "broken_links": broken_links,
    }
    print("\n==JSON_OUTPUT==")
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
