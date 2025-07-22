import pytest
from slackformat.richtext_converter import richtext_to_blockkit

class TestRichtextConverter:
    
    def test_simple_rich_text_section(self):
        """Test converting simple rich text section."""
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
        """Test bold text conversion."""
        richtext = {
            "type": "rich_text_section", 
            "elements": [{"type": "text", "text": "bold", "style": {"bold": True}}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*bold*"}
        }
        assert result == expected
    
    def test_italic_text(self):
        """Test italic text conversion."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "italic", "style": {"italic": True}}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "_italic_"}
        }
        assert result == expected
    
    def test_strike_text(self):
        """Test strike-through text conversion."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "strike", "style": {"strike": True}}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "~strike~"}
        }
        assert result == expected
    
    def test_code_text(self):
        """Test code text conversion."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "code", "style": {"code": True}}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "`code`"}
        }
        assert result == expected
    
    def test_multiple_styles(self):
        """Test text with multiple styles applied."""
        richtext = {
            "type": "rich_text_section",
            "elements": [
                {
                    "type": "text", 
                    "text": "bold italic", 
                    "style": {"bold": True, "italic": True}
                }
            ]
        }
        result = richtext_to_blockkit(richtext)
        # Should apply both styles - order matters for readability
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "_*bold italic*_"}
        }
        assert result == expected
    
    def test_link_with_custom_text(self):
        """Test link with custom display text."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "link", "url": "https://example.com", "text": "Example"}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "<https://example.com|Example>"}
        }
        assert result == expected
    
    def test_link_without_custom_text(self):
        """Test link without custom display text."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "link", "url": "https://example.com", "text": "https://example.com"}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "<https://example.com>"}
        }
        assert result == expected
    
    def test_emoji(self):
        """Test emoji conversion."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "emoji", "name": "smile"}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": ":smile:"}
        }
        assert result == expected
    
    def test_user_mention(self):
        """Test user mention conversion."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "user", "user_id": "U12345"}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "<@U12345>"}
        }
        assert result == expected
    
    def test_channel_mention(self):
        """Test channel mention conversion."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "channel", "channel_id": "C12345"}]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "<#C12345>"}
        }
        assert result == expected
    
    def test_mixed_elements(self):
        """Test mixed text and other elements."""
        richtext = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "Hello "},
                {"type": "text", "text": "world", "style": {"bold": True}},
                {"type": "text", "text": " and "},
                {"type": "link", "url": "https://example.com", "text": "link"}
            ]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Hello *world* and <https://example.com|link>"}
        }
        assert result == expected
    
    def test_rich_text_with_multiple_sections(self):
        """Test rich_text with multiple sections."""
        richtext = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": "First section"}]
                },
                {
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": "Second section"}]
                }
            ]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "First section\nSecond section"}
        }
        assert result == expected
    
    def test_bullet_list(self):
        """Test bullet list conversion."""
        richtext = {
            "type": "rich_text_list",
            "style": "bullet",
            "elements": [
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "Item 1"}]},
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "Item 2"}]}
            ]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "• Item 1\n• Item 2"}
        }
        assert result == expected
    
    def test_ordered_list(self):
        """Test ordered list conversion."""
        richtext = {
            "type": "rich_text_list",
            "style": "ordered",
            "elements": [
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "First"}]},
                {"type": "rich_text_section", "elements": [{"type": "text", "text": "Second"}]}
            ]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "1. First\n2. Second"}
        }
        assert result == expected
    
    def test_list_with_formatting(self):
        """Test list items with formatting."""
        richtext = {
            "type": "rich_text_list",
            "style": "bullet",
            "elements": [
                {
                    "type": "rich_text_section", 
                    "elements": [
                        {"type": "text", "text": "Item with "},
                        {"type": "text", "text": "bold", "style": {"bold": True}}
                    ]
                }
            ]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "• Item with *bold*"}
        }
        assert result == expected
    
    def test_empty_input(self):
        """Test empty input handling."""
        result = richtext_to_blockkit({})
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": ""}
        }
        assert result == expected
    
    def test_none_input(self):
        """Test None input handling."""
        result = richtext_to_blockkit(None)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": ""}
        }
        assert result == expected
    
    def test_unknown_element_type(self):
        """Test handling of unknown element types."""
        richtext = {
            "type": "rich_text_section",
            "elements": [{"type": "unknown", "text": "fallback text"}]
        }
        result = richtext_to_blockkit(richtext)
        # Should use fallback text handling
        assert result["text"]["text"] == "fallback text"