"""
Shared helper functions for parsing and tree traversals.
"""
import re
from typing import Dict, List, Any, Union, Optional

def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text, preserving intentional line breaks."""
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # Remove trailing/leading whitespace from lines
    lines = [line.strip() for line in text.split('\n')]
    return '\n'.join(lines)

def escape_markdown(text: str) -> str:
    """Escape special markdown characters in text."""
    special_chars = ['*', '_', '~', '`', '<', '>', '|', '[', ']', '(', ')']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def unescape_markdown(text: str) -> str:
    """Unescape markdown characters."""
    special_chars = ['*', '_', '~', '`', '<', '>', '|', '[', ']', '(', ')']
    for char in special_chars:
        text = text.replace(f'\\{char}', char)
    return text

def merge_text_elements(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge consecutive text elements with the same style."""
    if not elements:
        return elements
    
    merged = []
    current_element = None
    
    for element in elements:
        if element.get("type") == "text" and current_element and current_element.get("type") == "text":
            # Check if styles match
            current_style = current_element.get("style", {})
            element_style = element.get("style", {})
            
            if current_style == element_style:
                # Merge text
                current_element["text"] += element["text"]
                continue
        
        # Can't merge, add previous element and start new one
        if current_element:
            merged.append(current_element)
        current_element = element.copy()
    
    # Add the last element
    if current_element:
        merged.append(current_element)
    
    return merged

def split_text_by_delimiter(text: str, delimiter: str) -> List[str]:
    """Split text by delimiter, handling escaped delimiters."""
    parts = []
    current = ""
    i = 0
    
    while i < len(text):
        if text[i:i+len(delimiter)] == delimiter:
            # Check if it's escaped
            if i > 0 and text[i-1] == '\\':
                # Escaped delimiter, add to current
                current = current[:-1] + delimiter  # Remove backslash
            else:
                # Real delimiter, split here
                parts.append(current)
                current = ""
            i += len(delimiter)
        else:
            current += text[i]
            i += 1
    
    # Add remaining text
    if current:
        parts.append(current)
    
    return parts

def find_matching_delimiter(text: str, start: int, open_delim: str, close_delim: str = None) -> int:
    """Find the matching closing delimiter, handling nesting."""
    if close_delim is None:
        close_delim = open_delim
    
    depth = 1
    i = start + len(open_delim)
    
    while i < len(text) and depth > 0:
        if text[i:i+len(open_delim)] == open_delim:
            depth += 1
            i += len(open_delim)
        elif text[i:i+len(close_delim)] == close_delim:
            depth -= 1
            if depth == 0:
                return i
            i += len(close_delim)
        else:
            i += 1
    
    return -1

def extract_style_from_element(element: Dict[str, Any]) -> Dict[str, bool]:
    """Extract style information from an element."""
    return element.get("style", {})

def apply_style_to_text(text: str, style: Dict[str, bool]) -> str:
    """Apply markdown formatting to text based on style dict."""
    result = text
    
    if style.get("code"):
        result = f"`{result}`"
    if style.get("bold"):
        result = f"*{result}*"
    if style.get("italic"):
        result = f"_{result}_"
    if style.get("strike"):
        result = f"~{result}~"
    
    return result

def validate_rich_text_structure(obj: Dict[str, Any]) -> bool:
    """Validate that an object has a valid rich text structure."""
    if not isinstance(obj, dict):
        return False
    
    obj_type = obj.get("type")
    if obj_type not in ["rich_text", "rich_text_section", "rich_text_list"]:
        return False
    
    if obj_type == "rich_text":
        # Should have elements array
        elements = obj.get("elements", [])
        if not isinstance(elements, list):
            return False
        # Each element should be a valid rich text section/list
        for element in elements:
            if not validate_rich_text_structure(element):
                return False
    
    elif obj_type == "rich_text_section":
        # Should have elements array
        elements = obj.get("elements", [])
        if not isinstance(elements, list):
            return False
        # Each element should be a valid text element
        for element in elements:
            if not isinstance(element, dict) or not element.get("type"):
                return False
    
    elif obj_type == "rich_text_list":
        # Should have elements array and style
        elements = obj.get("elements", [])
        style = obj.get("style")
        if not isinstance(elements, list) or style not in ["bullet", "ordered"]:
            return False
    
    return True

def validate_blockkit_structure(obj: Dict[str, Any]) -> bool:
    """Validate that an object has a valid Block Kit structure."""
    if not isinstance(obj, dict):
        return False
    
    obj_type = obj.get("type")
    valid_types = ["section", "divider", "image", "actions", "context", "header", "rich_text"]
    
    if obj_type not in valid_types:
        return False
    
    # Basic validation for common block types
    if obj_type == "section":
        text = obj.get("text")
        if not isinstance(text, dict) or text.get("type") not in ["plain_text", "mrkdwn"]:
            return False
    
    return True

def clean_empty_elements(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove empty text elements from a list."""
    cleaned = []
    for element in elements:
        if element.get("type") == "text" and not element.get("text", "").strip():
            continue
        cleaned.append(element)
    return cleaned

def count_formatting_depth(text: str, char: str) -> int:
    """Count the depth of nested formatting characters."""
    depth = 0
    i = 0
    while i < len(text) and text[i] == char:
        depth += 1
        i += 1
    return depth