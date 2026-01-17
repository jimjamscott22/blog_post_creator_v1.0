"""
Export utilities for converting generated content to different formats
"""
from typing import Optional
from datetime import datetime
import base64


def generate_markdown(title: str, content: str, metadata: Optional[dict] = None) -> str:
    """
    Generate formatted Markdown from content
    
    Args:
        title: Document title
        content: Main content
        metadata: Optional metadata dict to include
    
    Returns:
        Formatted markdown string
    """
    md = f"# {title}\n\n"
    
    if metadata:
        md += "## Metadata\n\n"
        for key, value in metadata.items():
            if key not in ['provider']:  # Skip some internal fields
                md += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        md += f"\n*Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n\n"
        md += "---\n\n"
    
    md += content
    return md


def generate_html(title: str, content: str, metadata: Optional[dict] = None) -> str:
    """
    Generate HTML from content
    
    Args:
        title: Document title
        content: Main content (assumed to be markdown)
        metadata: Optional metadata dict to include
    
    Returns:
        HTML string
    """
    # Simple markdown to HTML conversion
    html_content = content.replace("\n#", "<h1>").replace("#", "<h1>")
    html_content = html_content.replace("**", "<strong>")
    html_content = html_content.replace("*", "<em>")
    html_content = html_content.replace("\n", "<br>")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
                color: #333;
            }}
            h1 {{ color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 10px; }}
            h2 {{ color: #155a8a; margin-top: 30px; }}
            code {{ background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; }}
            pre {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            .metadata {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 30px; }}
            .metadata p {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
    """
    
    if metadata:
        html += '<div class="metadata"><h3>Metadata</h3>'
        for key, value in metadata.items():
            if key not in ['provider']:
                html += f"<p><strong>{key.replace('_', ' ').title()}:</strong> {value}</p>"
        html += f"<p><em>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</em></p>"
        html += "</div>"
    
    html += f"<div class='content'>{html_content}</div></body></html>"
    return html


def create_download_button_markdown(filename: str, content: str) -> tuple:
    """
    Create download data for markdown file
    
    Args:
        filename: Output filename
        content: File content
    
    Returns:
        Tuple of (content, filename, mime_type)
    """
    return content, filename, "text/markdown"


def create_download_button_html(filename: str, content: str) -> tuple:
    """
    Create download data for HTML file
    
    Args:
        filename: Output filename
        content: File content
    
    Returns:
        Tuple of (content, filename, mime_type)
    """
    return content, filename.replace('.md', '.html'), "text/html"


def create_download_button_txt(filename: str, content: str) -> tuple:
    """
    Create download data for plain text file
    
    Args:
        filename: Output filename
        content: File content
    
    Returns:
        Tuple of (content, filename, mime_type)
    """
    return content, filename.replace('.md', '.txt'), "text/plain"
