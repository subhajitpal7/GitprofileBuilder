"""
Module for building GitHub profile README.md from resume PDFs.
This module handles the process of extracting information from resumes and generating
attractive GitHub profile READMEs.
"""

import json
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Dict, Optional, Union
from pathlib import Path
from gitprofilebuilder.profile_generator import ProfileGenerator
from gitprofilebuilder.templates import get_template, template_manager
from gitprofilebuilder.config import Config

# Set up logging
logger = logging.getLogger(__name__)

def load_resume(pdf_path: str) -> str:
    """
    Load and process the resume PDF.
    
    Args:
        pdf_path (str): Path to the resume PDF file
        
    Returns:
        str: Extracted text content from the PDF
    """
    loader = PyPDFium2Loader(pdf_path)
    pages = loader.load()
    return "\n\n".join(page.page_content for page in pages)

def build_readme_from_resume(pdf_path: str) -> Dict:
    """
    Main function to build GitHub README from a resume PDF.
    Extracts information from the resume and structures it for profile generation.
    
    Args:
        pdf_path (str): Path to the resume PDF file
        
    Returns:
        Dict: Structured data extracted from the resume
    """
    # Get config instance and validate
    config = Config()
    config.validate_config()
    
    # Load the document
    resume_text = load_resume(pdf_path)
    
    # Define improved prompt template for information extraction
    template = """
    Analyze the following resume text and extract key information in a structured format.
    
    Resume Text:
    {context}
    
    Please extract and return the following information in JSON format:
    {{
        "personal_info": {{
            "name": "Full name of the person",
            "email": "Email address if available",
            "phone": "Phone number if available",
            "location": "Location if available"
        }},
        "summary": "Professional summary or objective",
        "work_experience": [
            {{
                "company": "Company name",
                "title": "Job title",
                "duration": "Employment period",
                "responsibilities": ["Key responsibilities and achievements"]
            }}
        ],
        "education": [
            {{
                "degree": "Degree name",
                "institution": "Institution name",
                "graduation_year": "Year of graduation"
            }}
        ],
        "skills": {{
            "technical_skills": ["List of technical skills"],
            "soft_skills": ["List of soft skills"]
        }},
        "certifications": ["List of certifications if any"]
    }}
    
    Focus on extracting the most relevant and impressive information that would make a great GitHub profile.
    """
    
    # Set up the LLM and parsing pipeline
    prompt = PromptTemplate(template=template, input_variables=["context"])
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    chain = prompt | llm | JsonOutputParser()
    
    # Extract and structure the resume data
    try:
        structured_data = chain.invoke({"context": resume_text})
        return structured_data
    except Exception as e:
        raise Exception(f"Failed to parse resume: {str(e)}")

def generate_and_save_readme(
    pdf_path: Union[str, Path],
    output_path: Union[str, Path] = "README.md",
    template_name: str = "minimal",
    verbose: bool = False
) -> Optional[Dict]:
    """
    Generate a GitHub profile README from a resume and save it.
    
    Args:
        pdf_path (Union[str, Path]): Path to the resume PDF file
        output_path (Union[str, Path], optional): Path to save the README. 
                                                Defaults to "README.md".
        template_name (str, optional): Template to use. Defaults to "minimal".
        verbose (bool, optional): Whether to return intermediate data. Defaults to False.
    
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
    # Convert paths to Path objects
    pdf_path = Path(pdf_path)
    output_path = Path(output_path)
    
    # Validate resume exists
    if not pdf_path.exists():
        raise FileNotFoundError(f"Resume not found at {pdf_path}")
    
    # Validate template
    template_name = get_template(template_name)
    
    # Generate profile data
    generator = ProfileGenerator()
    profile_data = generator.generate_profile(str(pdf_path))
    
    # Render template
    readme_content = template_manager.render_template(template_name, profile_data)
    
    # Save to file
    output_path.write_text(readme_content, encoding='utf-8')
    
    # Return intermediate data if verbose
    if verbose:
        return {
            'resume_text': generator.resume_text,
            'structured_data': generator.structured_data,
            'enhanced': profile_data.get('enhanced', {})
        }
    
    return None