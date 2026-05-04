class SearchEngine:
    def __init__(self, inverted_index):
        """
        Args:
            inverted_index (dict): structure produced by Indexer
        """
        self.index = inverted_index

    def print_word(self, word):
        """
        Return the inverted index entry for a single word.
        Case-insensitive.
        """
        word = word.lower()
        return self.index.get(word, {})

    def find(self, query):
        """
        Multi-word AND search.
        Returns a list of URLs that contain ALL words in the query.

        Example:
            query = "good friends"
            → returns pages containing BOTH "good" AND "friends"
        """
        words = [w.lower() for w in query.split() if w.strip()]

        if not words:
            return []

        # Start with pages containing the first word
        first_word = words[0]
        if first_word not in self.index:
            return []

        result_pages = set(self.index[first_word].keys())

        # Intersect with pages containing each subsequent word
        for word in words[1:]:
            if word not in self.index:
                return []
            pages = set(self.index[word].keys())
            result_pages &= pages  # AND operation

            if not result_pages:
                return []

        return sorted(result_pages)


if __name__ == "__main__":
    # Example usage (for debugging)
    sample_index = {
        "good": {
            "https://example.com/page1": {"freq": 2, "positions": [0, 5]},
            "https://example.com/page2": {"freq": 1, "positions": [3]},
        },
        "friends": {
            "https://example.com/page1": {"freq": 1, "positions": [2]},
        }
    }

    engine = SearchEngine(sample_index)
    print(engine.print_word("good"))
    print(engine.find("good friends"))
