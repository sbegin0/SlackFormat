import pytest
from slackformat.converters.richtext_to_blockkit import richtext_to_blockkit

class TestRichtextToBlockkitConverter:
    
    def test_simple_rich_text_section(self):
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "Hello world"}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Hello world"}
        }
        assert result == expected

    def test_bold_text(self):
        richtext = {
            "type": "rich_text_section", 
            "elements": [{"type": "text", "text": "bold", "style": {"bold": True}}]
        }
        result = richtext_to_blockkit(richtext)
        assert result["text"]["text"] == "*bold*"

    def test_multiple_styles(self):
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "bold italic", "style": {"bold": True, "italic": True}}]
        }
        result = richtext_to_blockkit(richtext)
        assert result["text"]["text"] == "_*bold italic*_"

    def test_link_with_custom_text(self):
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "link", "url": "https://example.com", "text": "Example"}]
        }
        result = richtext_to_blockkit(richtext)
        assert result["text"]["text"] == "<https://example.com|Example>"

    def test_user_mention(self):
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "user", "user_id": "U12345"}]
        }
        result = richtext_to_blockkit(richtext)
        assert result["text"]["text"] == "<@U12345>"

    def test_bullet_list(self):
        richtext = {
            "type": "rich_text_list",
            "style": "bullet",
            "elements": [
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "Item 1"}]},
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "Item 2"}]}
            ]
        }
        result = richtext_to_blockkit(richtext)
        assert result["text"]["text"] == "• Item 1\n• Item 2"

    def test_empty_input(self):
        result = richtext_to_blockkit({})
        assert result["text"]["text"] == ""