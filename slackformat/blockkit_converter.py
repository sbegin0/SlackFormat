import re
from typing import Dict, List, Any

def blockkit_to_richtext(blockkit_obj: dict) -> dict:
    """
    Converts Block Kit JSON to Slack Rich Text object.

    Args:
        blockkit_obj (dict): Block Kit JSON

    Returns:
        dict: Slack Rich Text object
    """
    if not blockkit_obj or not isinstance(blockkit_obj, dict):
        return {"type": "rich_text_section", "elements": []}
    
    block_type = blockkit_obj.get("type", "")
    
    if block_type == "section":
        return _convert_section_block(blockkit_obj)
    elif block_type == "rich_text":
        # Already a rich text block
        return blockkit_obj
    elif block_type == "divider":
        return {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": "---"}]
        }
    elif block_type == "header":
        return _convert_header_block(blockkit_obj)
    elif block_type == "context":
        return _convert_context_block(blockkit_obj)
    else:
        # Fallback - try to extract any text
        text_content = _extract_text_from_block(blockkit_obj)
        return {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": text_content}] if text_content else []
        }

def _convert_section_block(section: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a section block to rich text."""
    text_obj = section.get("text", {})
    
    if text_obj.get("type") == "mrkdwn":
        # Convert markdown to rich text elements
        markdown_text = text_obj.get("text", "")
        return _markdown_to_richtext(markdown_text)
    elif text_obj.get("type") == "plain_text":
        # Plain text
        plain_text = text_obj.get("text", "")
        return {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": plain_text}]
        }
    else:
        # Fallback
        text_content = str(text_obj.get("text", "")) if isinstance(text_obj, dict) else str(text_obj)
        return {
            "type": "rich_text_section",
            "elements": [{"type": "text", "text": text_content}] if text_content else []
        }

def _convert_header_block(header: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a header block to rich text."""
    text_obj = header.get("text", {})
    text_content = text_obj.get("text", "") if isinstance(text_obj, dict) else str(text_obj)
    
    # Headers are typically bold in rich text
    return {
        "type": "rich_text_section",
        "elements": [
            {"type": "text", "text": text_content, "style": {"bold": True}}
        ] if text_content else []
    }

def _convert_context_block(context: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a context block to rich text."""
    elements = context.get("elements", [])
    rich_elements = []
    
    for element in elements:
        if element.get("type") == "mrkdwn":
            markdown_text = element.get("text", "")
            # Parse markdown inline
            parsed = _parse_markdown_inline(markdown_text)
            rich_elements.extend(parsed)
        elif element.get("type") == "plain_text":
            plain_text = element.get("text", "")
            if plain_text:
                rich_elements.append({"type": "text", "text": plain_text})
        else:
            text_content = _extract_text_from_block(element)
            if text_content:
                rich_elements.append({"type": "text", "text": text_content})
    
    return {
        "type": "rich_text_section",
        "elements": rich_elements
    }

def _markdown_to_richtext(markdown: str) -> Dict[str, Any]:
    """Convert markdown text to rich text object."""
    if not markdown or not markdown.strip():
        return {"type": "rich_text_section", "elements": []}
    
    # Split by lines for lists and blocks
    lines = markdown.split('\n')
    sections = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for list items
        if re.match(r'^[•\-\*]\s+', line):
            list_text = re.sub(r'^[•\-\*]\s+', '', line)
            elements = _parse_markdown_inline(list_text)
            if elements:
                sections.append({
                    "type": "rich_text_list",
                    "style": "bullet",
                    "elements": [{
                        "type": "rich_text_section",
                        "elements": elements
                    }]
                })
        elif re.match(r'^\d+\.\s+', line):
            list_text = re.sub(r'^\d+\.\s+', '', line)
            elements = _parse_markdown_inline(list_text)
            if elements:
                sections.append({
                    "type": "rich_text_list",
                    "style": "ordered",
                    "elements": [{
                        "type": "rich_text_section", 
                        "elements": elements
                    }]
                })
        else:
            # Regular text with inline formatting
            elements = _parse_markdown_inline(line)
            if elements:
                sections.append({
                    "type": "rich_text_section",
                    "elements": elements
                })
    
    if len(sections) > 1:
        return {
            "type": "rich_text",
            "elements": sections
        }
    elif len(sections) == 1:
        return sections[0]
    else:
        return {"type": "rich_text_section", "elements": []}

def _parse_markdown_inline(text: str) -> List[Dict[str, Any]]:
    """Parse inline markdown formatting."""
    if not text:
        return []
        
    elements = []
    i = 0
    
    while i < len(text):
        # Handle plain text until we find a special character
        next_special = _find_next_markdown_char(text, i)
        if next_special == -1:
            # No more special characters, add remaining text
            remaining_text = text[i:]
            if remaining_text:
                elements.append({"type": "text", "text": remaining_text})
            break
        elif next_special > i:
            # Add plain text before the special character
            plain_text = text[i:next_special]
            if plain_text:
                elements.append({"type": "text", "text": plain_text})
            i = next_special
            continue

        # Bold: *text* or **text**
        if text[i:i+2] == '**':
            end = text.find('**', i + 2)
            if end != -1 and end > i + 2:
                bold_text = text[i+2:end]
                elements.append({"type": "text", "text": bold_text, "style": {"bold": True}})
                i = end + 2
            else:
                # Unclosed **, treat as text
                elements.append({"type": "text", "text": text[i:]})
                break
        elif text[i] == '*':
            end = text.find('*', i + 1)
            if end != -1 and end > i + 1:
                bold_text = text[i+1:end]
                elements.append({"type": "text", "text": bold_text, "style": {"bold": True}})
                i = end + 1
            else:
                # Unclosed *, treat as text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        # Italic: _text_
        elif text[i] == '_':
            end = text.find('_', i + 1)
            if end != -1 and end > i + 1:
                italic_text = text[i+1:end]
                elements.append({"type": "text", "text": italic_text, "style": {"italic": True}})
                i = end + 1
            else:
                # Unclosed _, treat as text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        # Strike: ~text~
        elif text[i] == '~':
            end = text.find('~', i + 1)
            if end != -1 and end > i + 1:
                strike_text = text[i+1:end]
                elements.append({"type": "text", "text": strike_text, "style": {"strike": True}})
                i = end + 1
            else:
                # Unclosed ~, treat as text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        # Code: `text`
        elif text[i] == '`':
            end = text.find('`', i + 1)
            if end != -1 and end > i + 1:
                code_text = text[i+1:end]
                elements.append({"type": "text", "text": code_text, "style": {"code": True}})
                i = end + 1
            else:
                # Unclosed `, treat as text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        # Links: <url|text> or <url>
        elif text[i] == '<':
            end = text.find('>', i)
            if end != -1 and end > i + 1:
                link_content = text[i+1:end]
                if '|' in link_content:
                    parts = link_content.split('|', 1)
                    url, display_text = parts[0].strip(), parts[1].strip()
                    if url and display_text:
                        elements.append({
                            "type": "link",
                            "url": url,
                            "text": display_text
                        })
                    else:
                        # Malformed link, treat as text
                        elements.append({"type": "text", "text": text[i:end+1]})
                else:
                    url = link_content.strip()
                    if url:
                        elements.append({
                            "type": "link", 
                            "url": url,
                            "text": url
                        })
                    else:
                        # Empty link, treat as text
                        elements.append({"type": "text", "text": text[i:end+1]})
                i = end + 1
            else:
                # Unclosed <, treat as text
                elements.append({"type": "text", "text": text[i:]})
                break
        else:
            # Not a special character, treat as text
            elements.append({"type": "text", "text": text[i]})
            i += 1

    return elements

def _find_next_markdown_char(text: str, start: int) -> int:
    """Find the next markdown special character."""
    special_chars = ['*', '_', '~', '`', '<']
    positions = []
    for char in special_chars:
        pos = text.find(char, start)
        if pos != -1:
            positions.append(pos)
    return min(positions) if positions else -1

def _extract_text_from_block(block: Any) -> str:
    """Extract any text content from a block object."""
    if isinstance(block, str):
        return block
    elif isinstance(block, dict):
        # Look for common text fields
        for field in ['text', 'value', 'content', 'title']:
            if field in block:
                value = block[field]
                if isinstance(value, str):
                    return value
                elif isinstance(value, dict) and 'text' in value:
                    return str(value['text'])
        # Recursively search for text
        for value in block.values():
            if isinstance(value, (str, dict, list)):
                result = _extract_text_from_block(value)
                if result:
                    return result
    elif isinstance(block, list) and block:  # Only process non-empty lists
        for item in block:
            result = _extract_text_from_block(item)
            if result:
                return result
    
    return ""