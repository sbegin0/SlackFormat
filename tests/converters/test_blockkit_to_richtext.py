import pytest
from slackformat.converters.blockkit_to_richtext import blockkit_to_richtext

class TestBlockkitToRichtextConverter:
    
    def test_section_with_mrkdwn(self):
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*bold* text"}
        }
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "bold", "style": {"bold": True}},
                {"type": "text", "text": " text"}
            ]
        }
        assert result == expected

    def test_section_with_plain_text(self):
        blockkit = {
            "type": "section",
            "text": {"type": "plain_text", "text": "Plain text"}
        }
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "Plain text"}]
        }
        assert result == expected

    def test_header_block(self):
        blockkit = {
            "type": "header",
            "text": {"type": "plain_text", "text": "Header Text"}
        }
        result = blockkit_to_richtext(blockkit)
        assert result["elements"][0]["text"] == "Header Text"
        assert result["elements"][0]["style"]["bold"] is True

    def test_context_block(self):
        blockkit = {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "*Context* text"}]
        }
        result = blockkit_to_richtext(blockkit)
        assert result["elements"][0]["text"] == "Context"
        assert result["elements"][0]["style"]["bold"] is True

    def test_rich_text_passthrough(self):
        rich_text = {
            "type": "rich_text",
            "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": "Passthrough"}]}]
        }
        result = blockkit_to_richtext(rich_text)
        assert result == rich_text

    def test_empty_blockkit(self):
        assert blockkit_to_richtext(None) == {"type": "rich_text_section", "elements": []}