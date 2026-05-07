from random import sample

from search import SearchEngine

sample_index = {
    "good": {
        "url1": {"freq": 2, "positions": [0, 3]},
        "url2": {"freq": 1, "positions": [5]},
    },
    "friends": {
        "url1": {"freq": 1, "positions": [1]},
    },
    "hello": {
        "u1": {"freq": 1, "positions": [0]}
    },
    "world": {
        "u1": {"freq": 1, "positions": [1]},
        "u2": {"freq": 2, "positions": [0, 3]}
    }
}

def test_print_word():
    engine = SearchEngine(sample_index)
    entry = engine.print_word("good")
    assert "url1" in entry
    assert entry["url1"]["freq"] == 2

def test_print_word_not_found():
    engine = SearchEngine(sample_index)
    assert engine.print_word("banana") == {}

def test_find_single_word():
    engine = SearchEngine(sample_index)
    pages = engine.find("good")
    assert pages == ["url1", "url2"]

def test_find_multiword_and():
    engine = SearchEngine(sample_index)
    pages = engine.find("good friends")
    assert pages == ["url1"]

def test_find_no_results():
    engine = SearchEngine(sample_index)
    pages = engine.find("good banana")
    assert pages == []

def test_find_empty_query():
    engine = SearchEngine(sample_index)
    assert engine.find("") == []

def test_find_ignores_extra_spaces():
    engine = SearchEngine(sample_index)
    assert engine.find("   hello   world   ") == ["u1"]

def test_find_case_insensitive():
    engine = SearchEngine(sample_index)
    assert engine.find("HeLLo WoRLd") == ["u1"]

def test_find_duplicate_words():
    engine = SearchEngine(sample_index)
    assert engine.find("world world") == ["u1", "u2"]

def test_find_word_not_in_index():
    engine = SearchEngine(sample_index)
    assert engine.find("banana") == []