import pytest
from slackformat.blockkit_md_converter import (
    blockkit_to_markdown,
    convert_blockkit_blocks_to_markdown,
    normalize_markdown_output
)

class TestBlockkitMarkdownConverter:
    
    def test_section_with_mrkdwn(self):
        """Test converting section block with markdown text."""
        blockkit = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*bold* text"}
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "*bold* text"
    
    def test_section_with_plain_text(self):
        """Test converting section block with plain text."""
        blockkit = {
            "type": "section",
            "text": {"type": "plain_text", "text": "Plain text with *special* chars"}
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Plain text with \\*special\\* chars"
    
    def test_header_block(self):
        """Test converting header block."""
        blockkit = {
            "type": "header",
            "text": {"type": "plain_text", "text": "Header Text"}
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "## Header Text"
    
    def test_divider_block(self):
        """Test converting divider block."""
        blockkit = {"type": "divider"}
        result = blockkit_to_markdown(blockkit)
        assert result == "---"
    
    def test_context_block(self):
        """Test converting context block."""
        blockkit = {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": "*Context* text"},
                {"type": "plain_text", "text": " and plain"}
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "_*Context* text and plain_"
    
    def test_image_block_with_title(self):
        """Test converting image block with title."""
        blockkit = {
            "type": "image",
            "image_url": "https://example.com/image.jpg",
            "alt_text": "Example Image",
            "title": {"type": "plain_text", "text": "My Image"}
        }
        result = blockkit_to_markdown(blockkit)
        assert result == '![Example Image](https://example.com/image.jpg "My Image")'
    
    def test_image_block_without_title(self):
        """Test converting image block without title."""
        blockkit = {
            "type": "image",
            "image_url": "https://example.com/image.jpg",
            "alt_text": "Example Image"
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "![Example Image](https://example.com/image.jpg)"
    
    def test_image_block_no_url(self):
        """Test converting image block without URL."""
        blockkit = {
            "type": "image",
            "alt_text": "Missing Image"
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "*[Missing Image]*"
    
    def test_rich_text_section(self):
        """Test converting rich text section with various formatting."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": "Hello "},
                        {"type": "text", "text": "bold", "style": {"bold": True}},
                        {"type": "text", "text": " and "},
                        {"type": "text", "text": "italic", "style": {"italic": True}},
                        {"type": "text", "text": " text"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Hello **bold** and *italic* text"
    
    def test_rich_text_with_links(self):
        """Test converting rich text with links."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": "Visit "},
                        {"type": "link", "url": "https://example.com", "text": "our site"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Visit [our site](https://example.com)"
    
    def test_rich_text_with_code(self):
        """Test converting rich text with code formatting."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": "Use "},
                        {"type": "text", "text": "print()", "style": {"code": True}},
                        {"type": "text", "text": " function"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Use `print()` function"
    
    def test_rich_text_bullet_list(self):
        """Test converting rich text bullet list."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_list",
                    "style": "bullet",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [{"type": "text", "text": "First item"}]
                        },
                        {
                            "type": "rich_text_section", 
                            "elements": [{"type": "text", "text": "Second item"}]
                        }
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "- First item\n- Second item"
    
    def test_rich_text_ordered_list(self):
        """Test converting rich text ordered list."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_list",
                    "style": "ordered",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [{"type": "text", "text": "First step"}]
                        },
                        {
                            "type": "rich_text_section",
                            "elements": [{"type": "text", "text": "Second step"}]
                        }
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "1. First step\n2. Second step"
    
    def test_rich_text_quote(self):
        """Test converting rich text quote."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_quote",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [{"type": "text", "text": "This is a quote"}]
                        }
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "> This is a quote"
    
    def test_rich_text_preformatted(self):
        """Test converting rich text preformatted code block."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_preformatted",
                    "elements": [
                        {"type": "text", "text": "def hello():\n    print('Hello World')"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "```\ndef hello():\n    print('Hello World')\n```"
    
    def test_combined_formatting(self):
        """Test combined bold and italic formatting."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text", 
                            "text": "bold italic", 
                            "style": {"bold": True, "italic": True}
                        }
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "***bold italic***"
    
    def test_strikethrough_formatting(self):
        """Test strikethrough formatting."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": "strikethrough",
                            "style": {"strike": True}
                        }
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "~~strikethrough~~"
    
    def test_emoji_conversion(self):
        """Test emoji conversion."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": "Hello "},
                        {"type": "emoji", "name": "wave"},
                        {"type": "text", "text": " World"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Hello :wave: World"
    
    def test_user_mention(self):
        """Test user mention conversion."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": "Hello "},
                        {"type": "user", "user_id": "U12345"},
                        {"type": "text", "text": "!"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Hello <@U12345>!"
    
    def test_channel_mention(self):
        """Test channel mention conversion."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": "Check "},
                        {"type": "channel", "channel_id": "C12345"},
                        {"type": "text", "text": " channel"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Check <#C12345> channel"
    
    def test_broadcast_mention(self):
        """Test broadcast mention conversion."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "broadcast", "range": "here"},
                        {"type": "text", "text": " attention please"}
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "@here attention please"
    
    def test_multiple_blocks_conversion(self):
        """Test converting multiple blocks."""
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Title"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Some *bold* text"}
            },
            {"type": "divider"}
        ]
        result = convert_blockkit_blocks_to_markdown(blocks)
        assert result == "## Title\n\nSome *bold* text\n\n---"
    
    def test_empty_input(self):
        """Test with empty or None input."""
        assert blockkit_to_markdown(None) == ""
        assert blockkit_to_markdown({}) == ""
        assert convert_blockkit_blocks_to_markdown([]) == ""
        assert convert_blockkit_blocks_to_markdown(None) == ""
    
    def test_unknown_block_type(self):
        """Test unknown block type handling."""
        blockkit = {"type": "unknown", "text": "some content"}
        result = blockkit_to_markdown(blockkit)
        assert result == "some content"
    
    def test_complex_nested_structure(self):
        """Test complex nested text extraction."""
        blockkit = {
            "type": "custom",
            "data": {
                "text": "extracted text",
                "nested": {"content": "nested content"}
            },
            "elements": [{"value": "element value"}]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "extracted text"
    
    def test_markdown_escaping(self):
        """Test that special characters are properly escaped."""
        blockkit = {
            "type": "section",
            "text": {"type": "plain_text", "text": "Text with *asterisks* and _underscores_"}
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "Text with \\*asterisks\\* and \\_underscores\\_"
    
    def test_normalize_markdown_output(self):
        """Test markdown output normalization."""
        markdown = "\n\n\nTitle\n\n\n\nContent\n\n\n"
        result = normalize_markdown_output(markdown)
        assert result == "Title\n\nContent"
    
    def test_mixed_rich_text_elements(self):
        """Test rich text with mixed element types."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": "Section 1"}]
                },
                {
                    "type": "rich_text_list",
                    "style": "bullet",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [{"type": "text", "text": "List item"}]
                        }
                    ]
                },
                {
                    "type": "rich_text_quote",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [{"type": "text", "text": "Quote text"}]
                        }
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        expected = "Section 1\n\n- List item\n\n> Quote text"
        assert result == expected
    
    def test_nested_list_formatting(self):
        """Test list with formatted text inside."""
        blockkit = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_list",
                    "style": "bullet",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {"type": "text", "text": "Item with "},
                                {"type": "text", "text": "bold", "style": {"bold": True}},
                                {"type": "text", "text": " text"}
                            ]
                        }
                    ]
                }
            ]
        }
        result = blockkit_to_markdown(blockkit)
        assert result == "- Item with **bold** text"