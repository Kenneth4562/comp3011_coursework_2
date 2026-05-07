from crawler import Crawler
from unittest.mock import patch, MagicMock

FAKE_HTML_PAGE_1 = """
<html>
<body>
    <span class="text">“Good friends are good for your soul.”</span>
    <li class="next"><a href="/page/2/">Next</a></li>
</body>
</html>
"""

FAKE_HTML_PAGE_2 = """
<html>
<body>
    <span class="text">“Life is short, smile while you still have teeth.”</span>
</body>
</html>
"""

def fake_get(url, timeout=10):
    mock = MagicMock()
    if "page/2" in url:
        mock.text = FAKE_HTML_PAGE_2
    else:
        mock.text = FAKE_HTML_PAGE_1
    mock.raise_for_status.return_value = None
    return mock

@patch("crawler.requests.get", side_effect=fake_get)
@patch("crawler.time.sleep", return_value=None)  # skip 6-second delay
def test_crawler_collects_pages(mock_sleep, mock_get):
    crawler = Crawler()
    pages = crawler.crawl()

    assert len(pages) == 2
    assert "Good friends" in pages["https://quotes.toscrape.com"]
    assert "Life is short" in pages["https://quotes.toscrape.com/page/2/"]

def test_extract_text():
    crawler = Crawler()
    soup = crawler._extract_text

def fake_response(text):
    mock = MagicMock()
    mock.text = text
    mock.raise_for_status.return_value = None
    return mock

@patch("crawler.time.sleep", return_value=None)
def test_crawler_handles_missing_quote_tags(mock_sleep):
    html = "<html><body><p>No quotes here</p></body></html>"
    with patch("crawler.requests.get", return_value=fake_response(html)):
        crawler = Crawler()
        pages = crawler.crawl()
        assert list(pages.values())[0] == ""  # empty text extracted

@patch("crawler.time.sleep", return_value=None)
def test_crawler_stops_when_no_next_page(mock_sleep):
    html = """
    <html><body>
        <span class="text">“Hello world”</span>
        <!-- No next button -->
    </body></html>
    """
    with patch("crawler.requests.get", return_value=fake_response(html)):
        crawler = Crawler()
        pages = crawler.crawl()
        assert len(pages) == 1