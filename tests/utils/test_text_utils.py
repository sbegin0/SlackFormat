import pytest
from slackformat.utils.text_utils import (
    normalize_whitespace, 
    escape_markdown_chars,
    normalize_markdown_output
)

class TestTextUtils:
    
    def test_normalize_whitespace(self):
        text = "Hello    world\n  test  "
        assert normalize_whitespace(text) == "Hello world\ntest"

    def test_escape_markdown_chars(self):
        text = "Hello *world* and `code`"
        assert escape_markdown_chars(text) == "Hello \\*world\\* and \\`code\\`"

    def test_normalize_markdown_output(self):
        markdown = "\n\nTitle\n\n\n\nContent\n"
        assert normalize_markdown_output(markdown) == "Title\n\nContent"