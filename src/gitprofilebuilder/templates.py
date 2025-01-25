"""
Template management for GitHub profile README generation.
"""

import os
import random
from pathlib import Path
from typing import Dict, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Constants
GREETINGS = [
    "👋 Hi there,",
    "🌟 Hello World,",
    "✨ Welcome,",
    "🚀 Hey there,",
    "💫 Greetings,",
]

COLORS = [
    "FF6B6B",  # Coral Red
    "4ECDC4",  # Turquoise
    "45B7D1",  # Sky Blue
    "96CEB4",  # Sage Green
    "D4A5A5",  # Dusty Rose
    "9B59B6",  # Purple
    "3498DB",  # Blue
    "E67E22",  # Orange
    "1ABC9C",  # Emerald
    "F1C40F",  # Yellow
]

class TemplateManager:
    """Manages GitHub profile README templates using Jinja2."""
    
    def __init__(self):
        """Initialize the template manager."""
        self.template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['code_format'] = lambda x: f'`{x}`'
        self.env.filters['urlencode'] = lambda x: x.replace(' ', '%20')
        
        # Add global functions
        self.env.globals['random_greeting'] = self._random_greeting
        self.env.globals['random_color'] = self._random_color
    
    def _random_greeting(self) -> str:
        """Get a random greeting."""
        return random.choice(GREETINGS)
    
    def _random_color(self) -> str:
        """Get a random color for badges."""
        return random.choice(COLORS)
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template names."""
        templates = []
        for file in self.template_dir.glob("*.md.j2"):
            templates.append(file.stem.replace('.md', ''))
        return templates
    
    def render_template(self, template_name: str, data: Dict) -> str:
        """
        Render a template with the provided data.
        
        Args:
            template_name (str): Name of the template to use (without extension)
            data (Dict): Data to populate the template with
        
        Returns:
            str: Rendered template content
        
        Raises:
            ValueError: If template doesn't exist
        """
        template_file = f"{template_name}.md.j2"
        if not (self.template_dir / template_file).exists():
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.env.get_template(template_file)
        return template.render(**data)

# Initialize the template manager
template_manager = TemplateManager()

def get_template(template_name: str = "minimal") -> str:
    """
    Get a GitHub profile README template.
    
    Args:
        template_name (str, optional): Name of the template to use. Defaults to "minimal".
        
    Returns:
        str: Template name if valid
        
    Raises:
        ValueError: If template name is invalid
    """
    available_templates = template_manager.get_available_templates()
    if template_name not in available_templates:
        raise ValueError(
            f"Invalid template name: {template_name}. "
            f"Available templates: {', '.join(available_templates)}"
        )
    return template_name

# Export available templates
TEMPLATES = {name: name for name in template_manager.get_available_templates()}
