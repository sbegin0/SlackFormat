def md_to_richtext(md_text: str) -> dict:
    """
    Converts Slack Markdown string to Slack Rich Text object.

    Args:
        md_text (str): Slack Markdown input

    Returns:
        dict: Slack Rich Text object
    """
    # Minimal manual parser for Slack Markdown to Rich Text
    # Only handles bold (*text*) for now, extensible for more
    import re
    elements = []
    i = 0
    while i < len(md_text):
        if md_text[i] == '*':
            # Find closing *
            end = md_text.find('*', i+1)
            if end != -1:
                text = md_text[i+1:end]
                elements.append({"type": "text", "text": text, "style": {"bold": True}})
                i = end + 1
            else:
                # Lone *
                elements.append({"type": "text", "text": "*"})
                i += 1
        else:
            # Find next * or end
            next_bold = md_text.find('*', i)
            if next_bold == -1:
                text = md_text[i:]
                elements.append({"type": "text", "text": text})
                break
            else:
                text = md_text[i:next_bold]
                if text:
                    elements.append({"type": "text", "text": text})
                i = next_bold

    return {"type": "rich_text_section", "elements": elements}
