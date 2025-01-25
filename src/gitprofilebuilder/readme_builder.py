"""
GitHub Profile README builder module.
"""

import logging
from pathlib import Path
from typing import Dict, Optional, Union

from .profile_generator import ProfileGenerator
from .templates import get_template, template_manager

# Set up logging
logger = logging.getLogger(__name__)

def generate_and_save_readme(
    resume_path: Union[str, Path],
    output_path: Union[str, Path] = "profile_readme.md",
    template_name: str = "minimal",
    verbose: bool = False,
) -> Optional[Dict]:
    """
    Generate a GitHub profile README from a resume and save it.
    
    Args:
        resume_path (Union[str, Path]): Path to the resume PDF file
        output_path (Union[str, Path], optional): Path to save the README. 
                                                Defaults to "profile_readme.md".
        template_name (str, optional): Template to use. Defaults to "minimal".
        verbose (bool, optional): Whether to show detailed logging messages. Defaults to False.
    
    Returns:
        Optional[Dict]: If verbose is True, returns a dictionary containing:
            - resume_text: Raw text extracted from resume
            - structured_data: Structured data extracted from resume
            - enhanced: Enhanced data from LLM processing
        If verbose is False, returns None
    
    Raises:
        FileNotFoundError: If resume file doesn't exist
        ValueError: If template name is invalid
    """
    try:
        # Set logging level based on verbose flag
        logger.setLevel(logging.INFO if verbose else logging.ERROR)
        
        # Convert paths to Path objects
        resume_path = Path(resume_path)
        output_path = Path(output_path)
        
        # Validate resume exists
        if not resume_path.exists():
            raise FileNotFoundError(f"Resume not found at {resume_path}")
        
        # Validate template
        template_name = get_template(template_name)
        
        # Generate profile data
        generator = ProfileGenerator(verbose=verbose)
        profile_data = generator.generate_profile(str(resume_path))
        
        # Render template
        readme_content = template_manager.render_template(template_name, profile_data)
        
        # Save to file
        output_path.write_text(readme_content, encoding='utf-8')
        if verbose:
            logger.info(f"Successfully generated GitHub profile at {output_path}")
        
        # Return intermediate data if verbose
        if verbose:
            return {
                'resume_text': generator.resume_text,
                'structured_data': generator.structured_data,
                'enhanced': profile_data.get('enhanced', {})
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Failed to generate profile: {str(e)}")
        raise