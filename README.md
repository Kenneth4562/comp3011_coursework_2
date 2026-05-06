# COMP3011 Coursework 2: Search Engine Tool

## Project Overview

This project implements a simple search engine for the website **https://quotes.toscrape.com/** as part of COMP3011: Web Services and Web Data.  
The tool performs three main tasks:

1. **Crawling** - Visits all pages on the target website, respecting a 6‑second politeness window.
2. **Indexing** - Builds an inverted index storing word frequencies and positions for each page.
3. **Searching** - Provides a command‑line interface to print index entries and find pages containing specific words or multi‑word queries.

The project is fully modular, with separate components for crawling, indexing, searching, and the CLI.

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Kenneth4562/comp3011_coursework_2.git
cd comp3011_coursework_2
```

### 2. Install dependencies
This project requires Python 3.9+ and the following libraries:
- requests
- beautifulsoup4
- pytest (for testing)

Install them using:
```bash
pip install -r requirements.txt
```

Or install individually:
``` bash
pip install requests
pip install beautifulsoup4
pip install pytest
```

### 3. Project structure
```
project/
  src/
    crawler.py
    indexer.py
    search.py
    main.py
  data/
    index.json (created after build)
  tests/
    test_crawler.py
    test_indexer.py
    test_search.py
  pytest.ini
  requirements.txt
  README.md
```
---
## Usage Instructions
Run the tool from inside the src/ directory:
```
cd src
python main.py
```

### The following commands are available:

#### 1. build
Crawls the website, builds the inverted index, and saves it to data/index.json.
``` bash
> build
```

#### 2. load
Loads the previously saved index into memory.
``` bash
> load
```

#### 3. print [word]
Displays the inverted index entry for a single word.

Example:
``` bash
> print good
```

Output includes:
- URLs containing the word
- Frequency
- Word positions

#### 4. find [query]
Performs a multi‑word AND search. Returns pages containing all words in the query.

Example:
``` bash
> find good friends
```

Edge cases:
- Unknown words return no results
- Empty queries return no results

---
## Testing Instructions
This project uses **pytest** for automated testing.

Run all tests from the project root:
``` bash
pytest
```

Tests cover:
- Crawler - HTML parsing, pagination, URL handling (with mocked requests)
- Indexer - tokenisation, frequency counting, position tracking, save/load
- Search Engine - single‑word search, multi‑word AND search, edge cases

To run a specific test file:
``` bash
pytest tests/test_search.py
```

---
## Notes
- The index file is automatically created in the data/ directory after running build.
- The index file must be built and loaded prior to any other functions working. 
- The crawler respects the required 6‑second politeness window.
- All components are modular and can be tested independently.