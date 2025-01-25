"""
Profile data generator for GitHub README profiles.
"""

import json
import logging
from typing import Dict, Optional
from pathlib import Path

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFium2Loader

from .config import Config

# Set up logging
logger = logging.getLogger(__name__)

# Define improved prompt templates
STRUCTURED_DATA_PROMPT = """
Analyze the following resume text and extract key information in a structured format.

Resume Text:
{resume_text}

Extract and return ONLY a JSON object with the following structure. Keep all text in a single line without line breaks:
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
Ensure all dates and durations are properly formatted.
For work experience, highlight achievements and impactful contributions.
For technical skills, group them by relevance and expertise level.
Keep all text responses concise and in a single line.
"""

ENHANCEMENT_PROMPT = """
Enhance this GitHub profile data with additional sections and improvements.
Make it engaging and memorable while maintaining professionalism.

Profile Data:
{profile_data}

Return ONLY a JSON object with the following structure. Keep all text in a single line without line breaks:
{{
    "enhanced": {{
        "tagline": "A creative one-liner that captures their essence as a developer",
        "impact_statement": "A powerful statement about their potential impact in tech",
        "current_focus": ["2-3 areas they're currently focusing on"],
        "collaboration_style": "A brief description of their collaboration approach",
        "github_activity_highlights": ["3-4 key points about GitHub activity"],
        "fun_facts": ["3-4 interesting facts"],
        "skill_categories": {{
            "category_name": ["Grouped skills from technical_skills"],
            "expertise_levels": ["Map of skills to expertise levels"]
        }},
        "custom_sections": [
            {{
                "title": "Section title with emoji",
                "content": ["2-3 points for this section"]
            }}
        ]
    }}
}}

Make the content engaging but factual, based on their actual experience and skills.
Keep all responses concise and in a single line without line breaks.
"""

class ProfileGenerator:
    """Generates GitHub profile data from resume."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the profile generator with configuration.
        
        Args:
            verbose (bool): Whether to show detailed logging messages
        """
        self.config = Config()
        self.config.validate_config()
        
        # Initialize model
        self.llm = GoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=self.config.GOOGLE_API_KEY,
            temperature=0.7
        )
        
        # Store intermediate data
        self.resume_text: Optional[str] = None
        self.structured_data: Optional[Dict] = None
        self.verbose = verbose
        
        # Set logging level based on verbose flag
        logger.setLevel(logging.INFO if verbose else logging.ERROR)
    
    def _log_info(self, message: str) -> None:
        """Log info message only if verbose mode is enabled."""
        if self.verbose:
            logger.info(message)
    
    def _log_error(self, message: str) -> None:
        """Log error message."""
        logger.error(message)
    
    def extract_resume_text(self, resume_path: str) -> str:
        """
        Extract text from a PDF resume.
        
        Args:
            resume_path (str): Path to the resume PDF file
        
        Returns:
            str: Extracted text from the resume
        """
        try:
            loader = PyPDFium2Loader(resume_path)
            pages = loader.load()
            self.resume_text = "\n".join(page.page_content for page in pages)
            self._log_info("Successfully extracted text from resume")
            return self.resume_text
        except Exception as e:
            self._log_error(f"Failed to extract text from resume: {str(e)}")
            raise
    
    def _clean_json_response(self, response: str) -> Dict:
        """Clean and parse JSON response from LLM."""
        try:
            # Remove any potential markdown code block markers
            response = response.replace("```json", "").replace("```", "").strip()
            # Parse the JSON
            return json.loads(response)
        except json.JSONDecodeError as e:
            self._log_error(f"Failed to parse JSON response: {str(e)}")
            raise
    
    def extract_structured_data(self) -> Dict:
        """
        Extract structured data from resume text using LLM.
        
        Returns:
            Dict: Structured data containing personal info, skills, experience, etc.
        """
        if not self.resume_text:
            raise ValueError("Resume text not extracted yet. Call extract_resume_text first.")
        
        try:
            # Generate structured data
            prompt = PromptTemplate(
                input_variables=["resume_text"],
                template=STRUCTURED_DATA_PROMPT
            )
            
            response = self.llm.invoke(prompt.format(resume_text=self.resume_text))
            self.structured_data = self._clean_json_response(response)
            self._log_info("Successfully extracted structured data")
            return self.structured_data
        except Exception as e:
            self._log_error(f"Failed to extract structured data: {str(e)}")
            raise
    
    def enhance_profile_data(self) -> Dict:
        """
        Enhance profile data with additional sections and improvements using LLM.
        
        Returns:
            Dict: Enhanced profile data with additional sections
        """
        if not self.structured_data:
            raise ValueError("Structured data not extracted yet. Call extract_structured_data first.")
        
        try:
            # Generate enhanced data
            prompt = PromptTemplate(
                input_variables=["profile_data"],
                template=ENHANCEMENT_PROMPT
            )
            
            response = self.llm.invoke(prompt.format(profile_data=json.dumps(self.structured_data)))
            enhanced_data = self._clean_json_response(response)
            
            # Merge enhanced data with original
            self.structured_data.update(enhanced_data)
            self._log_info("Successfully enhanced profile data")
            return self.structured_data
        except Exception as e:
            self._log_error(f"Failed to enhance profile data: {str(e)}")
            raise
    
    def generate_profile(self, resume_path: str) -> Dict:
        """
        Generate complete profile data from resume.
        
        Args:
            resume_path (str): Path to the resume PDF file
        
        Returns:
            Dict: Complete profile data ready for template rendering
        """
        try:
            # Extract text from resume
            self.extract_resume_text(resume_path)
            
            # Extract structured data
            self.extract_structured_data()
            
            # Enhance profile data
            profile_data = self.enhance_profile_data()
            
            self._log_info("Successfully generated complete profile")
            return profile_data
            
        except Exception as e:
            self._log_error(f"Failed to generate profile: {str(e)}")
            raise