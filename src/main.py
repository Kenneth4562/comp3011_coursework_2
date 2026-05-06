import os
import json

from crawler import Crawler
from indexer import Indexer
from search import SearchEngine


# Path to the project root (one level above src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the data folder at project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Full path to index file
INDEX_FILE = os.path.join(DATA_DIR, "index.json")


def command_build():
    print("[BUILD] Starting crawler...")
    crawler = Crawler()
    page_text = crawler.crawl()
    
    if page_text == {}:
        print("[BUILD] Error: No pages were crawled. Ensure the website is accessible (i.e., check your internet connection) Aborting index build.")
    else:
        print("[BUILD] Building inverted index...")
        indexer = Indexer()
        
        indexer.build_index(page_text)

        # Ensure data folder exists at project root
        os.makedirs(DATA_DIR, exist_ok=True)

        print(f"[BUILD] Saving index to {INDEX_FILE}...")
        indexer.save(INDEX_FILE)

        print("[BUILD] Done.")


def command_load():
    print(f"[LOAD] Loading index from {INDEX_FILE}...")
    try:
        indexer = Indexer()
        inverted_index = indexer.load(INDEX_FILE)
        print("[LOAD] Index loaded.")
        return inverted_index
    except FileNotFoundError:
        print(f"[ERROR] Index file not found at {INDEX_FILE}. Please run 'build' first.")
        return None


def command_print(engine, word):
    entry = engine.print_word(word)
    if not entry:
        print(f"[PRINT] Word '{word}' not found in index.")
    else:
        print(json.dumps(entry, indent=2))


def command_find(engine, query):
    pages = engine.find(query)
    if not pages:
        print("[FIND] No pages contain the query.")
    else:
        print("[FIND] Pages containing all words:")
        for p in pages:
            print(" -", p)


def main():
    print("COMP3011 Search Tool")
    print("Commands: build, load, print <word>, find <query>, exit")

    engine = None  # SearchEngine instance after loading index

    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()

        # -------------------------
        # BUILD
        # -------------------------
        if cmd == "build":
            command_build()

        # -------------------------
        # LOAD
        # -------------------------
        elif cmd == "load":
            inverted_index = command_load()
            engine = SearchEngine(inverted_index)

        # -------------------------
        # PRINT <word>
        # -------------------------
        elif cmd == "print":
            if engine is None:
                print("[ERROR] Load the index first using 'load'.")
                continue
            if len(parts) < 2:
                print("[ERROR] Usage: print <word>")
                continue
            word = parts[1]
            command_print(engine, word)

        # -------------------------
        # FIND <query>
        # -------------------------
        elif cmd == "find":
            if engine is None:
                print("[ERROR] Load the index first using 'load'.")
                continue
            if len(parts) < 2:
                print("[ERROR] Usage: find <query>")
                continue
            query = " ".join(parts[1:])
            command_find(engine, query)

        # -------------------------
        # EXIT
        # -------------------------
        elif cmd == "exit":
            print("Goodbye.")
            break

        else:
            print("[ERROR] Unknown command.")


if __name__ == "__main__":
    main()
