import pytest
from slackformat.blockkit_converter import blockkit_to_richtext

class TestBlockkitConverter:
    
    def test_section_with_mrkdwn(self):
        """Test converting section block with markdown text."""
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
        """Test converting section block with plain text."""
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
        """Test converting header block."""
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
        """Test converting divider block."""
        blockkit = {"type": "divider"}
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "---"}]
        }
        assert result == expected
    
    def test_context_block(self):
        """Test converting context block."""
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
    
    def test_markdown_formatting(self):
        """Test various markdown formatting conversions."""
        test_cases = [
            ("*bold*", [{"type": "text", "text": "bold", "style": {"bold": True}}]),
            ("_italic_", [{"type": "text", "text": "italic", "style": {"italic": True}}]),
            ("~strike~", [{"type": "text", "text": "strike", "style": {"strike": True}}]),
            ("`code`", [{"type": "text", "text": "code", "style": {"code": True}}]),
        ]
        
        for markdown, expected_elements in test_cases:
            blockkit = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": markdown}
            }
            result = blockkit_to_richtext(blockkit)
            assert result["elements"] == expected_elements
    
    def test_markdown_links(self):
        """Test markdown link conversion."""
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
    
    def test_markdown_link_without_text(self):
        """Test markdown link without display text."""
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Visit <https://example.com>"}
        }
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [
                {"type": "text", "text": "Visit "},
                {"type": "link", "url": "https://example.com", "text": "https://example.com"}
            ]
        }
        assert result == expected
    
    def test_bullet_list_conversion(self):
        """Test bullet list conversion from markdown."""
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "• First item\n• Second item"}
        }
        result = blockkit_to_richtext(blockkit)
        
        assert result["type"] == "rich_text"
        assert len(result["elements"]) == 2
        
        for element in result["elements"]:
            assert element["type"] == "rich_text_list"
            assert element["style"] == "bullet"
    
    def test_ordered_list_conversion(self):
        """Test ordered list conversion from markdown."""
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "1. First item\n2. Second item"}
        }
        result = blockkit_to_richtext(blockkit)
        
        assert result["type"] == "rich_text"
        assert len(result["elements"]) == 2
        
        for element in result["elements"]:
            assert element["type"] == "rich_text_list"
            assert element["style"] == "ordered"
    
    def test_mixed_formatting(self):
        """Test mixed formatting in one text."""
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "Hello *bold* and _italic_ text"}
        }
        result = blockkit_to_richtext(blockkit)
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
    
    def test_double_asterisk_bold(self):
        """Test **bold** formatting."""
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "**bold text**"}
        }
        result = blockkit_to_richtext(blockkit)
        expected = {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "bold text", "style": {"bold": True}}]
        }
        assert result == expected
    
    def test_empty_blockkit(self):
        """Test with empty or None input."""
        assert blockkit_to_richtext(None) == {"type": "rich_text_section", "elements": []}
        assert blockkit_to_richtext({}) == {"type": "rich_text_section", "elements": []}
    
    def test_unknown_block_type(self):
        """Test unknown block type handling."""
        blockkit = {"type": "unknown", "content": "some content"}
        result = blockkit_to_richtext(blockkit)
        
        # Should extract any available text and return a valid structure
        assert result["type"] == "rich_text_section"
        assert isinstance(result["elements"], list)
    
    def test_rich_text_passthrough(self):
        """Test that existing rich text blocks are passed through."""
        rich_text = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": "Already rich text"}]
                }
            ]
        }
        result = blockkit_to_richtext(rich_text)
        assert result == rich_text
    
    def test_nested_formatting_in_lists(self):
        """Test formatting within list items."""
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "• Item with *bold* text\n• Another _italic_ item"}
        }
        result = blockkit_to_richtext(blockkit)
        
        assert result["type"] == "rich_text"
        first_list = result["elements"][0]
        first_item_elements = first_list["elements"][0]["elements"]
        
        # Should have text + bold + text elements
        assert len(first_item_elements) == 3
        assert first_item_elements[1]["style"]["bold"] == True
    
    def test_malformed_markdown(self):
        """Test handling of malformed markdown."""
        test_cases = [
            "*unclosed bold",
            "_unclosed italic",
            "<incomplete link",
            "`unclosed code",
            "~~unclosed strike"
        ]
        
        for markdown in test_cases:
            blockkit = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": markdown}
            }
            result = blockkit_to_richtext(blockkit)
            
            # Should not crash and should return some valid structure
            assert result["type"] == "rich_text_section"
            assert isinstance(result["elements"], list)
    
    def test_complex_text_extraction(self):
        """Test text extraction from complex nested objects."""
        complex_block = {
            "type": "custom",
            "data": {
                "text": "extracted text",
                "nested": {
                    "content": "nested content"
                }
            },
            "elements": [
                {"value": "element value"}
            ]
        }
        result = blockkit_to_richtext(complex_block)
        
        # Should extract some text content
        assert result["type"] == "rich_text_section"
        assert len(result["elements"]) >= 1