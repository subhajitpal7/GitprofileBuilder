"""
Module for building GitHub profile README.md from resume PDFs.
This module handles the process of extracting information from resumes and generating
attractive GitHub profile READMEs.
"""

import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Dict
from gitprofilebuilder.profile_generator import generate_github_profile
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

def generate_and_save_readme(pdf_path: str, output_path: str = "README.md", 
                           template: str = "minimal") -> None:
    """
    Generate and save a GitHub profile README from a resume PDF.
    
    Args:
        pdf_path (str): Path to the resume PDF file
        output_path (str, optional): Path where to save the README.md. Defaults to "README.md"
        template (str, optional): Template style to use ('minimal' or 'modern'). 
                                Defaults to 'minimal'
    """
    try:
        # Extract structured data from resume
        resume_data = build_readme_from_resume(pdf_path)
        
        # Generate profile content
        profile_content = generate_github_profile(resume_data, template)
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(profile_content)
            
        logger.info(f"GitHub profile {output_path} has been generated successfully using {template} template!")
        
    except Exception as e:
        logger.error(f"Error generating profile: {str(e)}")
        raise