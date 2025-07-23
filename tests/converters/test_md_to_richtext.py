import pytest
from slackformat.converters.md_to_richtext import md_to_richtext

class TestMdToRichtextConverter:
    
    def test_empty_text(self):
        result = md_to_richtext("")
        expected = {"type": "rich_text_section", "elements": []}
        assert result == expected

    def test_plain_text(self):
        result = md_to_richtext("Hello world")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "Hello world"}]
        }
        assert result == expected

    def test_bold_text(self):
        result = md_to_richtext("*bold*")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "bold", "style": {"bold": True}}]
        }
        assert result == expected

    def test_italic_text(self):
        result = md_to_richtext("_italic_")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "italic", "style": {"italic": True}}]
        }
        assert result == expected

    def test_mixed_formatting(self):
        result = md_to_richtext("Hello *bold* and _italic_ text")
        expected = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "Hello "},
                {"type": "text", "text": "bold", "style": {"bold": True}},
                {"type": "text", "text": " and "},
                {"type": "text", "text": "italic", "style": {"italic": True}},
                {"type": "text", "text": " text"}
            ]
        }
        assert result == expected

    def test_bullet_list(self):
        result = md_to_richtext("• First item\n• Second item")
        assert result["type"] == "rich_text"
        assert result["elements"][0]["type"] == "rich_text_list"
        assert result["elements"][0]["style"] == "bullet"

    def test_unclosed_formatting(self):
        result = md_to_richtext("*unclosed bold")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "*unclosed bold"}]
        }
        assert result == expected