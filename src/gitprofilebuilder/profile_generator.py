"""
GitHub Profile README Generator with dynamic templates and LLM enhancement.
"""

from typing import Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from gitprofilebuilder.templates import get_template
from gitprofilebuilder.config import Config

class GitHubProfileGenerator:
    """
    A utility class for generating GitHub profile README.md content from structured resume data.
    This class is designed to be used as a helper by the resume parser module.
    """
    
    def __init__(self, resume_data: Dict):
        """
        Initialize the profile generator with resume data.
        
        Args:
            resume_data (Dict): Structured resume data containing personal info, skills, experience, etc.
        """
        self.resume_data = resume_data

    def generate_header(self) -> str:
        """Generate the header section with personal info and summary."""
        name = self.resume_data["personal_info"]["name"]
        summary = self.resume_data["summary"]
        
        return f"""# Hi there 👋, I'm {name}

{summary}
"""

    def generate_skills_section(self) -> str:
        """Generate the skills section."""
        tech_skills = self.resume_data["skills"]["technical_skills"]
        soft_skills = self.resume_data["skills"]["soft_skills"]
        
        skills_section = "## 🛠️ Skills\n\n"
        
        if tech_skills:
            skills_section += "### Technical Skills\n"
            skills_section += " | ".join(f"`{skill}`" for skill in tech_skills)
            skills_section += "\n\n"
        
        if soft_skills:
            skills_section += "### Soft Skills\n"
            skills_section += " | ".join(f"`{skill}`" for skill in soft_skills)
            skills_section += "\n"
            
        return skills_section

    def generate_experience_section(self) -> str:
        """Generate the work experience section."""
        experience = self.resume_data["work_experience"]
        
        if not experience:
            return ""
            
        exp_section = "## 💼 Experience\n\n"
        
        for job in experience:
            exp_section += f"### {job['title']} at {job['company']}\n"
            exp_section += f"*{job['duration']}*\n\n"
            
            if job['responsibilities']:
                for resp in job['responsibilities']:
                    exp_section += f"- {resp}\n"
            exp_section += "\n"
            
        return exp_section

    def generate_education_section(self) -> str:
        """Generate the education section."""
        education = self.resume_data["education"]
        
        if not education:
            return ""
            
        edu_section = "## 🎓 Education\n\n"
        
        for edu in education:
            edu_section += f"### {edu['degree']}\n"
            edu_section += f"{edu['institution']} - {edu['graduation_year']}\n\n"
            
        return edu_section

    def generate_certifications_section(self) -> str:
        """Generate the certifications section."""
        certs = self.resume_data["certifications"]
        
        if not certs:
            return ""
            
        cert_section = "## 📜 Certifications\n\n"
        for cert in certs:
            cert_section += f"- {cert}\n"
            
        return cert_section

    def generate_contact_section(self) -> str:
        """Generate the contact section."""
        info = self.resume_data["personal_info"]
        
        contact_section = "## 📫 How to reach me\n\n"
        
        if info.get("email"):
            contact_section += f"- 📧 Email: {info['email']}\n"
        if info.get("location"):
            contact_section += f"- 📍 Location: {info['location']}\n"
            
        return contact_section

    def generate_profile(self) -> str:
        """Generate the complete GitHub profile README."""
        sections = [
            self.generate_header(),
            self.generate_skills_section(),
            self.generate_experience_section(),
            self.generate_education_section(),
            self.generate_certifications_section(),
            self.generate_contact_section()
        ]
        
        return "\n".join(section for section in sections if section)

def enhance_content_with_llm(resume_data: Dict) -> Dict:
    """
    Use LLM to enhance resume data with creative and personalized content.
    
    Args:
        resume_data (Dict): Original resume data
        
    Returns:
        Dict: Enhanced resume data with additional creative elements
    """
    template = """
    You are a creative GitHub profile enhancer. Given the following resume data, generate engaging and personalized content
    to make the GitHub profile more attractive and memorable. Keep the tone professional yet friendly.
    
    Resume Data:
    {resume_data}
    
    Please enhance this data by adding the following elements in JSON format:
    {{
        "tagline": "A creative one-liner that captures their essence as a developer",
        "fun_facts": ["3-4 interesting facts about their skills, experience, or interests"],
        "current_focus": ["2-3 areas they're currently focusing on, based on their skills and experience"],
        "custom_sections": [
            {{
                "title": "Creative section title with emoji",
                "content": ["2-3 interesting points for this section"]
            }}
        ],
        "skill_categories": {{
            "category_name": ["grouped skills from their technical_skills, max 3 categories"],
            "expertise_levels": ["map of key skills to expertise levels like 'Expert', 'Advanced', 'Growing'"]
        }},
        "github_activity_highlights": ["3 key points about potential GitHub activity based on their background"],
        "collaboration_style": "A brief description of their likely collaboration style based on their experience",
        "impact_statement": "A powerful statement about their potential impact in tech"
    }}
    
    Make the content engaging but factual, based on their actual experience and skills.
    """
    
    try:
        # Setup LLM chain
        prompt = PromptTemplate(template=template, input_variables=["resume_data"])
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        chain = prompt | llm | JsonOutputParser()
        
        # Get enhanced content
        enhanced_data = chain.invoke({"resume_data": str(resume_data)})
        
        # Merge enhanced data with original resume data
        resume_data["enhanced"] = enhanced_data
        return resume_data
        
    except Exception as e:
        print(f"Warning: LLM enhancement failed: {str(e)}")
        # Return original data if enhancement fails
        return resume_data

def generate_github_profile(resume_data: Dict, template_name: str = "minimal") -> str:
    """
    Generate a GitHub profile README from resume data using specified template
    and LLM enhancement.
    
    Args:
        resume_data (Dict): Structured resume data containing personal info, skills, experience, etc.
        template_name (str, optional): Name of template to use ('minimal' or 'modern'). 
                                     Defaults to 'minimal'.
        
    Returns:
        str: Generated GitHub profile README content in markdown format
    """
    # First enhance the content using LLM
    enhanced_data = enhance_content_with_llm(resume_data)
    
    # Get the specified template
    template = get_template(template_name)
    
    # Generate profile content using the template and enhanced data
    return template.generate(enhanced_data)