import pytest
from slackformat.converters.md_to_blockkit import md_to_blockkit

class TestMdToBlockkitConverter:
    
    def test_simple_conversion(self):
        md = "Hello world"
        result = md_to_blockkit(md)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Hello world"}
        }
        assert result == expected

    def test_conversion_with_formatting(self):
        md = "Some *bold* and _italic_ text."
        result = md_to_blockkit(md)
        assert result["type"] == "section"
        assert result["text"]["text"] == "Some *bold* and _italic_ text."

    def test_list_conversion(self):
        md = "• Item 1\n• Item 2"
        result = md_to_blockkit(md)
        assert result["type"] == "section"
        assert result["text"]["text"] == "• Item 1\n• Item 2"