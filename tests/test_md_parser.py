import pytest
from slackformat import md_to_richtext, richtext_to_blockkit
from slackformat.blockkit_converter import blockkit_to_richtext
from slackformat.utils import (
    normalize_whitespace, escape_markdown, merge_text_elements, 
    validate_rich_text_structure, clean_empty_elements
)

# Test md_parser.py
class TestMdParser:
    
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
    
    def test_strike_text(self):
        result = md_to_richtext("~strike~")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "strike", "style": {"strike": True}}]
        }
        assert result == expected
    
    def test_code_text(self):
        result = md_to_richtext("`code`")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "code", "style": {"code": True}}]
        }
        assert result == expected
    
    def test_link_with_text(self):
        result = md_to_richtext("<https://example.com|Example>")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "link", "url": "https://example.com", "text": "Example"}]
        }
        assert result == expected
    
    def test_link_without_text(self):
        result = md_to_richtext("<https://example.com>")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "link", "url": "https://example.com", "text": "https://example.com"}]
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
        expected = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_list",
                    "style": "bullet",
                    "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": "First item"}]}]
                },
                {
                    "type": "rich_text_list", 
                    "style": "bullet",
                    "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": "Second item"}]}]
                }
            ]
        }
        assert result == expected
    
    def test_unclosed_formatting(self):
        result = md_to_richtext("*unclosed bold")
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "*unclosed bold"}]
        }
        assert result == expected


# Test richtext_converter.py
class TestRichtextConverter:
    
    def test_simple_text(self):
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
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*bold*"}
        }
        assert result == expected
    
    def test_link(self):
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
    
    def test_mixed_elements(self):
        richtext = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "Hello "},
                {"type": "text", "text": "world", "style": {"bold": True}}
            ]
        }
        result = richtext_to_blockkit(richtext)
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Hello *world*"}
        }
        assert result == expected
    
    def test_list(self):
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
    
    def test_empty_input(self):
        result = richtext_to_blockkit({})
        expected = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": ""}
        }
        assert result == expected


# Test blockkit_converter.py
class TestBlockkitConverter:
    
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
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "Header Text", "style": {"bold": True}}]
        }
        assert result == expected
    
    def test_divider_block(self):
        blockkit = {"type": "divider"}
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "---"}]
        }
        assert result == expected
    
    def test_context_block(self):
        blockkit = {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "*Context* text"},
                {"type": "plain_text", "text": " and plain"}
            ]
        }
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "Context", "style": {"bold": True}},
                {"type": "text", "text": " text"},
                {"type": "text", "text": " and plain"}
            ]
        }
        assert result == expected
    
    def test_markdown_links(self):
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Visit <https://example.com|our site>"}
        }
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "Visit "},
                {"type": "link", "url": "https://example.com", "text": "our site"}
            ]
        }
        assert result == expected
    
    def test_unknown_block_type(self):
        blockkit = {"type": "unknown", "content": "some content"}
        result = blockkit_to_richtext(blockkit)
        # Should extract any available text
        assert result["type"] == "rich_text_section"
        assert len(result["elements"]) >= 1


# Test utils.py
class TestUtils:
    
    def test_normalize_whitespace(self):
        text = "Hello    world\n  test  "
        result = normalize_whitespace(text)
        expected = "Hello world\ntest"
        assert result == expected
    
    def test_escape_markdown(self):
        text = "Hello *world* and _test_"
        result = escape_markdown(text)
        expected = "Hello \\*world\\* and \\_test\\_"
        assert result == expected
    
    def test_merge_text_elements(self):
        elements = [
            {"type": "text", "text": "Hello "},
            {"type": "text", "text": "world"},
            {"type": "text", "text": "bold", "style": {"bold": True}},
            {"type": "text", "text": " more bold", "style": {"bold": True}}
        ]
        result = merge_text_elements(elements)
        expected = [
            {"type": "text", "text": "Hello world"},
            {"type": "text", "text": "bold more bold", "style": {"bold": True}}
        ]
        assert result == expected
    
    def test_validate_rich_text_structure(self):
        valid_obj = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "Hello"}]
        }
        assert validate_rich_text_structure(valid_obj) == True
        
        invalid_obj = {"type": "invalid", "elements": []}
        assert validate_rich_text_structure(invalid_obj) == False
    
    def test_clean_empty_elements(self):
        elements = [
            {"type": "text", "text": "Hello"},
            {"type": "text", "text": ""},
            {"type": "text", "text": "   "},
            {"type": "text", "text": "world"}
        ]
        result = clean_empty_elements(elements)
        expected = [
            {"type": "text", "text": "Hello"},
            {"type": "text", "text": "world"}
        ]
        assert result == expected


# Integration tests
class TestIntegration:
    
    def test_roundtrip_md_to_richtext_to_blockkit(self):
        """Test converting markdown to rich text to blockkit."""
        md = "Hello *bold* and _italic_ text"
        richtext = md_to_richtext(md)
        blockkit = richtext_to_blockkit(richtext)
        
        assert blockkit["type"] == "section"
        assert "Hello *bold* and _italic_ text" in blockkit["text"]["text"]
    
    def test_roundtrip_blockkit_to_richtext_to_blockkit(self):
        """Test converting blockkit to rich text and back."""
        original_blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Bold* text"}
        }
        
        richtext = blockkit_to_richtext(original_blockkit)
        new_blockkit = richtext_to_blockkit(richtext)
        
        assert new_blockkit["type"] == "section"
        assert "*Bold* text" in new_blockkit["text"]["text"]
    
    def test_complex_formatting(self):
        """Test complex formatting combinations."""
        md = "Visit <https://example.com|our site> for *bold* and `code` examples"
        richtext = md_to_richtext(md)
        blockkit = richtext_to_blockkit(richtext)
        
        text = blockkit["text"]["text"]
        assert "<https://example.com|our site>" in text
        assert "*bold*" in text
        assert "`code`" in text
    
    def test_list_handling(self):
        """Test list conversion."""
        md = "• First item\n• Second item with *bold*"
        richtext = md_to_richtext(md)
        blockkit = richtext_to_blockkit(richtext)
        
        text = blockkit["text"]["text"]
        assert "• First item" in text
        assert "• Second item with *bold*" in text


# Performance and edge case tests
class TestEdgeCases:
    
    def test_very_long_text(self):
        """Test with very long text."""
        long_text = "A" * 10000
        result = md_to_richtext(long_text)
        assert result["type"] == "rich_text_section"
        assert result["elements"][0]["text"] == long_text
    
    def test_nested_formatting_prevention(self):
        """Test that nested formatting is handled gracefully."""
        md = "*bold _italic_ bold*"  # Nested formatting
        result = md_to_richtext(md)
        # Should handle this gracefully without breaking
        assert result["type"] == "rich_text_section"
    
    def test_malformed_links(self):
        """Test malformed links."""
        md = "<incomplete link"
        result = md_to_richtext(md)
        assert result["elements"][0]["text"] == "<incomplete link"
    
    def test_empty_formatting(self):
        """Test empty formatting markers."""
        md = "**"  # Empty bold
        result = md_to_richtext(md)
        assert result["elements"][0]["text"] == "**"
    
    def test_unicode_text(self):
        """Test with unicode characters."""
        md = "Hello 🌍 *世界*"
        result = md_to_richtext(md)
        richtext = richtext_to_blockkit(result)
        
        assert "🌍" in richtext["text"]["text"]
        assert "*世界*" in richtext["text"]["text"]


if __name__ == "__main__":
    pytest.main([__file__])