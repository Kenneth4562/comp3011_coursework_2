import json
import re
from collections import defaultdict


class Indexer:
    """
    Builds and stores an inverted index.
    """

    WORD_PATTERN = re.compile(r"[a-zA-Z]+")

    def __init__(self):
        # inverted_index[word][url] = {"freq": int, "positions": [int, ...]} - dictionary
        self.inverted_index = defaultdict(lambda: defaultdict(lambda: {"freq": 0, "positions": []}))

    def build_index(self, page_text):
        """
        Build the inverted index from crawler output.

        Args:
            page_text (dict): {url: text}
        """
        for url, text in page_text.items():
            tokens = self._tokenise(text)

            for position, word in enumerate(tokens):
                entry = self.inverted_index[word][url]
                entry["freq"] += 1
                entry["positions"].append(position)

        return self.inverted_index

    def _tokenise(self, text):
        """
        Convert raw text into a list of lowercase words.
        """
        words = self.WORD_PATTERN.findall(text.lower())
        return words

    def save(self, filepath):
        """
        Save the inverted index to a JSON file.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.inverted_index, f, indent=2)

    def load(self, filepath):
        """
        Load an inverted index from a JSON file.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            self.inverted_index = json.load(f)

        return self.inverted_index


if __name__ == "__main__":
    # Example usage (for debugging)
    sample = {
        "https://example.com": "Good friends are good people."
    }

    idx = Indexer()
    index = idx.build_index(sample)
    print(json.dumps(index, indent=2))
