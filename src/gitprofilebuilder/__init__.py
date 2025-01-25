"""
GitProfile Builder: Generate beautiful GitHub profile READMEs from resumes.
"""

from .readme_builder import generate_and_save_readme as gitprofilebuilder
from .cli import main
__all__ = ["gitprofilebuilder", "main"]