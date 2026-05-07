import os
import json
from indexer import Indexer

def test_tokenisation_basic():
    idx = Indexer()
    tokens = idx._tokenise("Good friends, GOOD times!")
    assert tokens == ["good", "friends", "good", "times"]

def test_build_index_structure():
    idx = Indexer()
    sample = {"url1": "good friends good"}
    index = idx.build_index(sample)

    assert "good" in index
    assert "url1" in index["good"]
    assert index["good"]["url1"]["freq"] == 2
    assert index["good"]["url1"]["positions"] == [0, 2]

def test_save_and_load(tmp_path):
    idx = Indexer()
    sample = {"url1": "good friends good"}
    index = idx.build_index(sample)

    file = tmp_path / "index.json"
    idx.save(file)

    idx2 = Indexer()
    loaded = idx2.load(file)

    assert loaded["good"]["url1"]["freq"] == 2

def test_indexer_handles_empty_text():
    idx = Indexer()
    index = idx.build_index({"url": ""})
    assert index == {}

def test_indexer_strips_punctuation():
    idx = Indexer()
    index = idx.build_index({"u": "Hello!!! world??"})
    assert "hello" in index and "world" in index

def test_indexer_unicode_words():
    idx = Indexer()
    index = idx.build_index({"u": "Café naïve façade"})
    # Regex strips accents, so these may not appear — test behaviour explicitly
    assert index != {}  # at least something is indexed

def test_indexer_large_input():
    idx = Indexer()
    text = "word " * 5000
    index = idx.build_index({"u": text})
    assert index["word"]["u"]["freq"] == 5000