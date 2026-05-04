import time
import requests
from bs4 import BeautifulSoup
from collections import deque


class Crawler:
    """
    A simple BFS crawler for quotes.toscrape.com.
    """

    BASE_URL = "https://quotes.toscrape.com"
    POLITENESS_SECONDS = 6

    def __init__(self):
        self.to_visit = deque([self.BASE_URL])
        self.visited = set()
        self.page_text = {}  # url -> extracted text

    def crawl(self):
        """
        Crawl all reachable pages starting from BASE_URL.
        Returns:
            dict: {url: extracted_text}
        """
        while self.to_visit:
            url = self.to_visit.popleft()

            if url in self.visited:
                continue

            print(f"[Crawler] Fetching: {url}")
            self.visited.add(url)

            html = self._fetch(url)
            if html is None:
                continue  # skip failed pages

            soup = BeautifulSoup(html, "html.parser")

            # Extract text content from the page
            text = self._extract_text(soup)
            self.page_text[url] = text

            # Discover next page link
            next_url = self._find_next_page(soup)
            if next_url and next_url not in self.visited:
                self.to_visit.append(next_url)

            # Respect politeness window
            time.sleep(self.POLITENESS_SECONDS)

        return self.page_text

    def _fetch(self, url):
        """
        Fetch HTML from a URL with error handling.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"[Crawler] Error fetching {url}: {e}")
            return None

    def _extract_text(self, soup):
        """
        Extract all quote text from the page.
        """
        quotes = soup.find_all("span", class_="text")
        extracted = " ".join(q.get_text(strip=True) for q in quotes)
        return extracted

    def _find_next_page(self, soup):
        """
        Find the URL of the next page, if it exists.
        """
        next_li = soup.find("li", class_="next")
        if not next_li:
            return None

        href = next_li.find("a")["href"]
        return f"{self.BASE_URL}{href}"


if __name__ == "__main__":
    crawler = Crawler()
    data = crawler.crawl()
    print("\nCrawling complete. Pages collected:")
    for url in data:
        print(" -", url)
