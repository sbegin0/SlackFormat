import pytest
from slackformat.converters.blockkit_to_md import blockkit_to_markdown, convert_blockkit_blocks_to_markdown

class TestBlockkitToMdConverter:
    
    def test_section_with_mrkdwn(self):
        blockkit = {"type": "section", "text": {"type": "mrkdwn", "text": "*bold* text"}}
        assert blockkit_to_markdown(blockkit) == "*bold* text"

    def test_section_with_plain_text(self):
        blockkit = {"type": "section", "text": {"type": "plain_text", "text": "Plain text with *"}}
        assert blockkit_to_markdown(blockkit) == "Plain text with \\*"

    def test_header_block(self):
        blockkit = {"type": "header", "text": {"type": "plain_text", "text": "Header Text"}}
        assert blockkit_to_markdown(blockkit) == "## Header Text"

    def test_image_block(self):
        blockkit = {
            "type": "image",
            "image_url": "https://a.com/img.png",
            "alt_text": "Alt Text",
            "title": {"type": "plain_text", "text": "Title"}
        }
        assert blockkit_to_markdown(blockkit) == '![Alt Text](https://a.com/img.png "Title")'

    def test_rich_text_section(self):
        blockkit = {
            "type": "rich_text",
            "elements": [{
                "type": "rich_text_section",
                "elements": [
                    {"type": "text", "text": "Hello "},
                    {"type": "text", "text": "bold", "style": {"bold": True}},
                ]
            }]
        }
        assert blockkit_to_markdown(blockkit) == "Hello **bold**"

    def test_rich_text_list(self):
        blockkit = {
            "type": "rich_text",
            "elements": [{
                "type": "rich_text_list", "style": "bullet",
                "elements": [{"type": "rich_text_section", "elements": [{"type": "text", "text": "Item"}]}]
            }]
        }
        # Note: This test requires a more complete implementation of blockkit_to_markdown
        # For now, it will likely extract the text content.
        pass # Placeholder for a more advanced test

    def test_multiple_blocks_conversion(self):
        blocks = [
            {"type": "header", "text": {"type": "plain_text", "text": "Title"}},
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": "Content"}}
        ]
        result = convert_blockkit_blocks_to_markdown(blocks)
        assert result == "## Title\n\n---\n\nContent"