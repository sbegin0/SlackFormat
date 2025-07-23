import re
from typing import Dict, List, Any, Union

def blockkit_to_markdown(blockkit_obj: dict) -> str:
    """
    Converts Block Kit JSON to Markdown text.

    Args:
        blockkit_obj (dict): Block Kit JSON

    Returns:
        str: Markdown formatted text
    """
    if not blockkit_obj or not isinstance(blockkit_obj, dict):
        return ""
    
    block_type = blockkit_obj.get("type", "")
    
    if block_type == "section":
        return _convert_section_block(blockkit_obj)
    elif block_type == "rich_text":
        return _convert_rich_text_block(blockkit_obj)
    elif block_type == "divider":
        return "---"
    elif block_type == "header":
        return _convert_header_block(blockkit_obj)
    elif block_type == "context":
        return _convert_context_block(blockkit_obj)
    elif block_type == "image":
        return _convert_image_block(blockkit_obj)
    else:
        # Fallback - try to extract any text
        text_content = _extract_text_from_block(blockkit_obj)
        return text_content

def _convert_section_block(section: Dict[str, Any]) -> str:
    """Convert a section block to markdown."""
    text_obj = section.get("text", {})
    
    if text_obj.get("type") == "mrkdwn":
        # Already markdown, just extract text
        return text_obj.get("text", "")
    elif text_obj.get("type") == "plain_text":
        # Plain text, escape markdown characters
        plain_text = text_obj.get("text", "")
        return _escape_markdown_chars(plain_text)
    else:
        # Fallback
        text_content = str(text_obj.get("text", "")) if isinstance(text_obj, dict) else str(text_obj)
        return _escape_markdown_chars(text_content)

def _convert_header_block(header: Dict[str, Any]) -> str:
    """Convert a header block to markdown header."""
    text_obj = header.get("text", {})
    text_content = text_obj.get("text", "") if isinstance(text_obj, dict) else str(text_obj)
    
    # Convert to markdown header (assuming level 2)
    return f"## {text_content}"

def _convert_context_block(context: Dict[str, Any]) -> str:
    """Convert a context block to markdown."""
    elements = context.get("elements", [])
    parts = []
    
    for element in elements:
        if element.get("type") == "mrkdwn":
            markdown_text = element.get("text", "")
            parts.append(markdown_text)
        elif element.get("type") == "plain_text":
            plain_text = element.get("text", "")
            parts.append(_escape_markdown_chars(plain_text))
        else:
            text_content = _extract_text_from_block(element)
            if text_content:
                parts.append(_escape_markdown_chars(text_content))
    
    # Context blocks are often smaller/secondary text
    result = "".join(parts)
    return f"_{result}_" if result else ""

def _convert_image_block(image: Dict[str, Any]) -> str:
    """Convert an image block to markdown image syntax."""
    image_url = image.get("image_url", "")
    alt_text = image.get("alt_text", "Image")
    title = image.get("title", {})
    
    if isinstance(title, dict):
        title_text = title.get("text", "")
    else:
        title_text = str(title) if title else ""
    
    if image_url:
        if title_text:
            return f"![{alt_text}]({image_url} \"{title_text}\")"
        else:
            return f"![{alt_text}]({image_url})"
    else:
        return f"*[{alt_text}]*"

def _convert_rich_text_block(rich_text: Dict[str, Any]) -> str:
    """Convert a rich text block to markdown."""
    elements = rich_text.get("elements", [])
    parts = []
    
    for element in elements:
        element_type = element.get("type", "")
        
        if element_type == "rich_text_section":
            parts.append(_convert_rich_text_section(element))
        elif element_type == "rich_text_list":
            parts.append(_convert_rich_text_list(element))
        elif element_type == "rich_text_quote":
            parts.append(_convert_rich_text_quote(element))
        elif element_type == "rich_text_preformatted":
            parts.append(_convert_rich_text_preformatted(element))
    
    return "\n\n".join(filter(None, parts))

def _convert_rich_text_section(section: Dict[str, Any]) -> str:
    """Convert a rich text section to markdown."""
    elements = section.get("elements", [])
    parts = []
    
    for element in elements:
        element_type = element.get("type", "")
        
        if element_type == "text":
            text = element.get("text", "")
            style = element.get("style", {})
            formatted_text = _apply_markdown_formatting(text, style)
            parts.append(formatted_text)
        elif element_type == "link":
            url = element.get("url", "")
            display_text = element.get("text", url)
            if url:
                parts.append(f"[{display_text}]({url})")
            else:
                parts.append(display_text)
        elif element_type == "emoji":
            emoji_name = element.get("name", "")
            if emoji_name:
                parts.append(f":{emoji_name}:")
        elif element_type == "channel":
            channel_id = element.get("channel_id", "")
            parts.append(f"<#{channel_id}>")
        elif element_type == "user":
            user_id = element.get("user_id", "")
            parts.append(f"<@{user_id}>")
        elif element_type == "broadcast":
            range_type = element.get("range", "here")
            parts.append(f"@{range_type}")
    
    return "".join(parts)

def _convert_rich_text_list(list_element: Dict[str, Any]) -> str:
    """Convert a rich text list to markdown list."""
    style = list_element.get("style", "bullet")
    elements = list_element.get("elements", [])
    list_items = []
    
    for i, item in enumerate(elements):
        if item.get("type") == "rich_text_section":
            item_text = _convert_rich_text_section(item)
            if style == "ordered":
                list_items.append(f"{i + 1}. {item_text}")
            else:  # bullet
                list_items.append(f"- {item_text}")
    
    return "\n".join(list_items)

def _convert_rich_text_quote(quote: Dict[str, Any]) -> str:
    """Convert a rich text quote to markdown blockquote."""
    elements = quote.get("elements", [])
    quote_parts = []
    
    for element in elements:
        if element.get("type") == "rich_text_section":
            quote_parts.append(_convert_rich_text_section(element))
    
    quote_text = "\n".join(quote_parts)
    # Convert to blockquote format
    lines = quote_text.split("\n")
    quoted_lines = [f"> {line}" for line in lines]
    return "\n".join(quoted_lines)

def _convert_rich_text_preformatted(preformatted: Dict[str, Any]) -> str:
    """Convert preformatted rich text to markdown code block."""
    elements = preformatted.get("elements", [])
    code_parts = []
    
    for element in elements:
        if element.get("type") == "text":
            code_parts.append(element.get("text", ""))
    
    code_text = "".join(code_parts)
    return f"```\n{code_text}\n```"

def _apply_markdown_formatting(text: str, style: Dict[str, bool]) -> str:
    """Apply markdown formatting to text based on style dict."""
    if not text:
        return text
    
    result = text
    
    # Apply formatting in specific order to handle nesting
    if style.get("code"):
        result = f"`{result}`"
    if style.get("bold"):
        result = f"**{result}**"
    if style.get("italic"):
        result = f"*{result}*"
    if style.get("strike"):
        result = f"~~{result}~~"
    
    return result

def _escape_markdown_chars(text: str) -> str:
    """Escape special markdown characters in plain text."""
    if not text:
        return text
    
    # Characters that need escaping in markdown
    special_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!', '|', '~']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def _extract_text_from_block(block: Any) -> str:
    """Extract any text content from a block object."""
    if isinstance(block, str):
        return block
    elif isinstance(block, dict):
        # Look for common text fields first
        if "text" in block:
            text = block["text"]
            if isinstance(text, str):
                return text
            elif isinstance(text, dict):
                return text.get("text", "")

        # Look through other common fields
        for field in ["value", "content", "title", "alt_text"]:
            if field in block:
                value = block[field]
                if isinstance(value, str):
                    return value
                elif isinstance(value, dict):
                    extracted = _extract_text_from_block(value)
                    if extracted:
                        return extracted
        
        # Recursively search for text in nested objects, but skip the 'type' field
        for key, value in block.items():
            if key == "type":  # Skip the type field to avoid returning block type names
                continue
            if isinstance(value, (str, dict, list)):
                result = _extract_text_from_block(value)
                if result:
                    return result
    elif isinstance(block, list) and block:
        for item in block:
            result = _extract_text_from_block(item)
            if result:
                return result
    
    return ""

def convert_blockkit_blocks_to_markdown(blocks: List[Dict[str, Any]]) -> str:
    """
    Convert a list of Block Kit blocks to markdown.
    
    Args:
        blocks (List[Dict[str, Any]]): List of Block Kit blocks
        
    Returns:
        str: Combined markdown text
    """
    if not blocks or not isinstance(blocks, list):
        return ""
    
    markdown_parts = []
    
    for block in blocks:
        markdown = blockkit_to_markdown(block)
        if markdown:
            markdown_parts.append(markdown)
    
    return "\n\n".join(markdown_parts)

def normalize_markdown_output(markdown: str) -> str:
    """Normalize markdown output by cleaning up excessive whitespace."""
    if not markdown:
        return ""
    
    # Remove excessive blank lines (more than 2 consecutive newlines)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    # Strip leading/trailing whitespace
    markdown = markdown.strip()
    
    return markdown