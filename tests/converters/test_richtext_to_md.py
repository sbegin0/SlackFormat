import pytest
from slackformat.converters.richtext_to_md import richtext_to_markdown

class TestRichtextToMdConverter:

    def test_simple_section(self):
        richtext = {"type": "rich_text_section", "elements": [{"type": "text", "text": "Hello"}]}
        assert richtext_to_markdown(richtext) == "Hello"

    def test_formatted_text(self):
        richtext = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "bold", "style": {"bold": True}},
                {"type": "text", "text": " and "},
                {"type": "text", "text": "italic", "style": {"italic": True}},
            ]
        }
        assert richtext_to_markdown(richtext) == "**bold** and *italic*"

    def test_link(self):
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "link", "url": "https://a.com", "text": "link"}]
        }
        assert richtext_to_markdown(richtext) == "[link](https://a.com)"

    def test_bullet_list(self):
        richtext = {
            "type": "rich_text_list", "style": "bullet",
            "elements": [
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "Item 1"}]},
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "Item 2"}]},
            ]
        }
        assert richtext_to_markdown(richtext) == "- Item 1\n- Item 2"