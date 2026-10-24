import requests
from bs4 import BeautifulSoup

# Browser-like headers so websites are less likely to reject the request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

# Max characters kept per page, so several pages fit in the model's context
MAX_CHARS = 6000


class WebScrap:
    def web_scraper(self, url: str) -> str:
        # 1) Send the request; any network failure becomes a clear error message
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}") from e

        # 2) Validate the response (outside the try block so these errors are not masked)
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code} (blocked or challenged?)")

        if "html" not in response.headers.get("Content-Type", ""):
            raise RuntimeError("Not an HTML page")

        # 3) Parse the HTML and remove menus and other non-content tags
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header",
                         "aside", "form", "noscript"]):
            tag.decompose()

        # 4) Prefer the main content container if the page has one
        main = soup.find("article") or soup.find("main") or soup.body or soup
        text = main.get_text(" ", strip=True)

        # 5) Fail with a clear message if nothing readable was found
        if not text.strip():
            raise RuntimeError("No readable text (JS-rendered or blocked)")

        # 6) Trim the text to the maximum length
        return text[:MAX_CHARS]