import pytest
from slackformat.md_parser import md_to_richtext

def test_bold_text():
    md = "*bold*"
    rich = md_to_richtext(md)
    expected = {
        "type": "rich_text_section",
        "elements": [
            {"type": "text", "text": "bold", "style": {"bold": True}}
        ]
    }
    assert rich == expected
