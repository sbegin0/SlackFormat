from typing import Dict, List, Any, Union

def richtext_to_blockkit(richtext_obj: dict) -> dict:
    """
    Converts Slack Rich Text object to Block Kit JSON.

    Args:
        richtext_obj (dict): Slack Rich Text object

    Returns:
        dict: Block Kit JSON representation
    """
    if not richtext_obj or not isinstance(richtext_obj, dict):
        return {"type": "section", "text": {"type": "mrkdwn", "text": ""}}
    
    # Handle different rich text types
    if richtext_obj.get("type") == "rich_text":
        # Multiple elements/sections
        markdown_text = _convert_rich_text_elements(richtext_obj.get("elements", []))
    elif richtext_obj.get("type") == "rich_text_section":
        # Single section
        markdown_text = _convert_rich_text_section(richtext_obj)
    elif richtext_obj.get("type") == "rich_text_list":
        # List
        markdown_text = _convert_rich_text_list(richtext_obj)
    else:
        # Fallback
        markdown_text = str(richtext_obj)
    
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": markdown_text
        }
    }

def _convert_rich_text_elements(elements: List[Dict[str, Any]]) -> str:
    """Convert a list of rich text elements to markdown."""
    result_parts = []
    
    for element in elements:
        if element.get("type") == "rich_text_section":
            result_parts.append(_convert_rich_text_section(element))
        elif element.get("type") == "rich_text_list":
            result_parts.append(_convert_rich_text_list(element))
        else:
            # Handle other types as needed
            result_parts.append("")
    
    return "\n".join(filter(None, result_parts))  # Filter out empty strings

def _convert_rich_text_section(section: Dict[str, Any]) -> str:
    """Convert a rich text section to markdown."""
    elements = section.get("elements", [])
    return _convert_text_elements(elements)

def _convert_rich_text_list(list_obj: Dict[str, Any]) -> str:
    """Convert a rich text list to markdown."""
    elements = list_obj.get("elements", [])
    list_style = list_obj.get("style", "bullet")
    
    result_parts = []
    for i, item in enumerate(elements):
        if item.get("type") == "rich_text_section":
            item_text = _convert_rich_text_section(item)
            if list_style == "ordered":
                result_parts.append(f"{i+1}. {item_text}")
            else:
                result_parts.append(f"• {item_text}")
        else:
            # Handle other item types
            item_text = str(item)
            if list_style == "ordered":
                result_parts.append(f"{i+1}. {item_text}")
            else:
                result_parts.append(f"• {item_text}")
    
    return "\n".join(result_parts)

def _convert_text_elements(elements: List[Dict[str, Any]]) -> str:
    """Convert text elements to markdown string."""
    result_parts = []
    
    for element in elements:
        element_type = element.get("type", "")
        
        if element_type == "text":
            text = element.get("text", "")
            style = element.get("style", {})
            
            # Apply formatting based on style - order matters for readability
            # Apply in order: code, bold, italic, strike (innermost to outermost)
            if style.get("code"):
                text = f"`{text}`"
            if style.get("bold"):
                text = f"*{text}*"
            if style.get("italic"):
                text = f"_{text}_"
            if style.get("strike"):
                text = f"~{text}~"
            
            result_parts.append(text)
            
        elif element_type == "link":
            url = element.get("url", "")
            link_text = element.get("text", url)
            if link_text == url:
                result_parts.append(f"<{url}>")
            else:
                result_parts.append(f"<{url}|{link_text}>")
                
        elif element_type == "emoji":
            name = element.get("name", "")
            result_parts.append(f":{name}:")
            
        elif element_type == "channel":
            channel_id = element.get("channel_id", "")
            result_parts.append(f"<#{channel_id}>")
            
        elif element_type == "user":
            user_id = element.get("user_id", "")
            result_parts.append(f"<@{user_id}>")
            
        else:
            # Fallback for unknown element types - try to extract text
            text = element.get("text", element.get("value", str(element)))
            result_parts.append(text)
    
    return "".join(result_parts)