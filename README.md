# SlackFormat

**SlackFormat** is a Python library that enables easy manipulation of Slack messages in any format. It provides a simple and intuitive way to convert between Slack's Markdown, Rich Text, and Block Kit formats.

-----

## Features

  * **Markdown to Rich Text:** Convert Slack's Markdown to a Rich Text object.
  * **Rich Text to Block Kit:** Convert a Rich Text object to a Block Kit JSON structure.
  * **Block Kit to Rich Text:** Convert Block Kit JSON to a Rich Text object.
  * **Comprehensive Formatting Support:** Supports various formatting options including bold, italic, strikethrough, code, links, and lists.

-----

## Installation

To install the library, you can use `pip`: (hopefully soon lol -- sorry to get ur hopes up)

```bash
pip install slackformat
```

-----

## Usage

Here are some examples of how to use the **SlackFormat** library.

### Markdown to Rich Text

You can convert a Markdown string to a Slack Rich Text object.

```python
from slackformat import md_to_richtext

md = "Hello *bold* and _italic_ text"
richtext = md_to_richtext(md)
print(richtext)
```

### Rich Text to Block Kit

You can convert a Rich Text object to a Block Kit JSON structure.

```python
from slackformat import richtext_to_blockkit

richtext = {
    "type": "rich_text_section",
    "elements": [
        {"type": "text", "text": "Hello "},
        {"type": "text", "text": "world", "style": {"bold": True}}
    ]
}
blockkit = richtext_to_blockkit(richtext)
print(blockkit)
```

### Block Kit to Rich Text

You can convert a Block Kit JSON structure to a Rich Text object.

```python
from slackformat.blockkit_converter import blockkit_to_richtext

blockkit = {
    "type": "section",
    "text": {"type": "mrkdwn", "text": "*Bold* text"}
}
richtext = blockkit_to_richtext(blockkit)
print(richtext)
```

-----

## Testing

To run the tests for this library, you can use `pytest`.

```bash
python -m pytest
```

The tests cover the following:

  * **Markdown Parser** (`tests/test_md_parser.py`): Tests for converting Markdown to Rich Text.
  * **Rich Text Converter** (`tests/test_richtext_converter.py`): Tests for converting Rich Text to Block Kit.
  * **Block Kit Converter** (`tests/test_blockkit_converter.py`): Tests for converting Block Kit to Rich Text.

-----

## License

This project is licensed under the Apache License 2.0.
