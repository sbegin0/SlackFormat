import re
from typing import List, Dict, Any

def md_to_richtext(md_text: str) -> dict:
    """
    Converts Slack Markdown string to Slack Rich Text object.
    
    Supports:
    - Bold: *text*
    - Italic: _text_
    - Strike: ~text~
    - Code: `text`
    - Links: <url|text> or <url>
    - Line breaks
    - Lists (basic)
    
    Args:
        md_text (str): Slack Markdown input

    Returns:
        dict: Slack Rich Text object
    """
    if not md_text:
        return {"type": "rich_text_section", "elements": []}
    
    # Split by lines to handle lists and line breaks
    lines = md_text.split('\n')
    sections = []
    
    for line_idx, line in enumerate(lines):
        if not line.strip():
            # Empty line - add line break if not the last line
            if line_idx < len(lines) - 1:
                sections.append({
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": "\n"}]
                })
            continue
            
        # Check if it's a list item
        list_match = re.match(r'^(\s*)([-*•]\s+)(.*)', line)
        if list_match:
            indent, bullet, content = list_match.groups()
            list_elements = _parse_inline_formatting(content)
            sections.append({
                "type": "rich_text_list",
                "style": "bullet",
                "elements": [{
                    "type": "rich_text_section",
                    "elements": list_elements
                }]
            })
        else:
            # Regular text with inline formatting
            elements = _parse_inline_formatting(line)
            sections.append({
                "type": "rich_text_section",
                "elements": elements
            })
    
    # If we have multiple sections, wrap in rich_text block
    if len(sections) > 1:
        return {
            "type": "rich_text",
            "elements": sections
        }
    elif len(sections) == 1:
        return sections[0]
    else:
        return {"type": "rich_text_section", "elements": []}

def _parse_inline_formatting(text: str) -> List[Dict[str, Any]]:
    """Parse inline formatting like bold, italic, code, links."""
    elements = []
    i = 0
    
    while i < len(text):
        # Check for different markdown patterns
        if text[i] == '*' and i + 1 < len(text):
            # Bold text
            end = _find_closing_delimiter(text, i, '*')
            if end != -1:
                # Check for empty content between markers
                if end == i + 1:
                    # Empty **|* markers, treat as literal text
                    elements.append({"type": "text", "text": text[i:end + 1]})
                    i = end + 1
                else:
                    bold_text = text[i+1:end]
                    elements.append({
                        "type": "text", 
                        "text": bold_text, 
                        "style": {"bold": True}
                    })
                    i = end + 1
            else:
                # Unclosed *, treat as plain text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        elif text[i] == '_' and i + 1 < len(text):
            # Italic text
            end = _find_closing_delimiter(text, i, '_')
            if end != -1:
                # Check for empty content between markers
                if end == i + 1:
                    # Empty _ markers, treat as literal text
                    elements.append({"type": "text", "text": text[i:end + 1]})
                    i = end + 1
                else:
                    italic_text = text[i+1:end]
                    elements.append({
                        "type": "text", 
                        "text": italic_text, 
                        "style": {"italic": True}
                    })
                    i = end + 1
            else:
                # Unclosed _, treat as plain text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        elif text[i] == '~' and i + 1 < len(text):
            # Strike-through text
            end = _find_closing_delimiter(text, i, '~')
            if end != -1:
                # Check for empty content between markers
                if end == i + 1:
                    # Empty ~ markers, treat as literal text
                    elements.append({"type": "text", "text": text[i:end + 1]})
                    i = end + 1
                else:
                    strike_text = text[i+1:end]
                    elements.append({
                        "type": "text", 
                        "text": strike_text, 
                        "style": {"strike": True}
                    })
                    i = end + 1
            else:
                # Unclosed ~, treat as plain text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        elif text[i] == '`' and i + 1 < len(text):
            # Code text
            end = _find_closing_delimiter(text, i, '`')
            if end != -1:
                # Check for empty content between markers
                if end == i + 1:
                    # Empty ` markers, treat as literal text
                    elements.append({"type": "text", "text": text[i:end + 1]})
                    i = end + 1
                else:
                    code_text = text[i+1:end]
                    elements.append({
                        "type": "text", 
                        "text": code_text, 
                        "style": {"code": True}
                    })
                    i = end + 1
            else:
                # Unclosed `, treat as plain text
                elements.append({"type": "text", "text": text[i:]})
                break
                
        elif text[i] == '<' and i + 1 < len(text):
            # Link
            end = text.find('>', i)
            if end != -1:
                # Check for empty content between < >
                if end == i + 1:
                    # Empty <> markers, treat as literal text
                    elements.append({"type": "text", "text": text[i:end + 1]})
                    i = end + 1
                else:
                    link_content = text[i+1:end]
                    if '|' in link_content:
                        url, display_text = link_content.split('|', 1)
                        if url.strip() and display_text.strip():
                            elements.append({
                                "type": "link",
                                "url": url.strip(),
                                "text": display_text.strip()
                            })
                        else:
                            # Invalid link content, treat as text
                            elements.append({"type": "text", "text": text[i:end + 1]})
                    else:
                        if link_content.strip():
                            elements.append({
                                "type": "link",
                                "url": link_content.strip(),
                                "text": link_content.strip()
                            })
                        else:
                            # Empty link content, treat as text
                            elements.append({"type": "text", "text": text[i:end + 1]})
                    i = end + 1
            else:
                # Unclosed <, treat as plain text
                elements.append({"type": "text", "text": text[i:]})
                break
        
        # Find the next special character or end of string
        next_special = _find_next_special_char(text, i)
        if next_special == -1:
            # Rest of the string is plain text
            if i < len(text):
                elements.append({"type": "text", "text": text[i:]})
            break
        else:
            # Add plain text up to the special character
            if next_special > i:
                elements.append({"type": "text", "text": text[i:next_special]})
            i = next_special
    
    return elements

def _find_closing_delimiter(text: str, start: int, delimiter: str) -> int:
    """Find the closing delimiter, handling escaped delimiters."""
    i = start + 1
    while i < len(text):
        if text[i] == delimiter:
            return i
        i += 1
    return -1

def _find_next_special_char(text: str, start: int) -> int:
    """Find the next special markdown character."""
    special_chars = ['*', '_', '~', '`', '<']
    positions = []
    for char in special_chars:
        pos = text.find(char, start)
        if pos != -1:
            positions.append(pos)
    return min(positions) if positions else -1