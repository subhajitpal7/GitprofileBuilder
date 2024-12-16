from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Dict
from gitprofilebuilder.profile_generator import generate_github_profile
from gitprofilebuilder.config import Config

def load_resume(pdf_path: str) -> str:
    """Load and process the resume PDF."""
    loader = PyPDFium2Loader(pdf_path)
    pages = loader.load()
    # Combine all pages into a single text
    return "\n\n".join(page.page_content for page in pages)

def parse_resume(pdf_path: str) -> Dict:
    """Main function to parse resume and return structured data."""
    # Validate configuration
    Config.validate_config()
    
    # Load the document
    resume_text = load_resume(pdf_path)
    print(resume_text)
    # Define improved prompt template
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

    Ensure all dates and durations are formatted consistently and all lists are properly formatted.
    If any information is not available in the resume, use null for that field.
    """

    # Setup the parsing chain
    prompt = PromptTemplate.from_template(template)
    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.1,
        google_api_key=Config.GOOGLE_API_KEY
    )
    chain = prompt | model | JsonOutputParser()

    # Process the resume
    try:
        result = chain.invoke({"context": resume_text})
        return result
    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        return None

def main():
    pdf_path = input("Enter the path to the resume PDF: ")
    try:
        resume_data = parse_resume(pdf_path)
        if resume_data:
            # Generate GitHub profile README
            profile_content = generate_github_profile(resume_data)
            
            # Save to README.md
            with open('README.md', 'w') as f:
                f.write(profile_content)
                
            print("Resume parsed and GitHub profile README.md has been generated successfully!")
            print("\nGenerated profile content:")
            print("-" * 50)
            print(profile_content)
        else:
            print("Failed to parse resume.")
    except Exception as e:
        print(f"Error processing resume: {str(e)}")

if __name__ == "__main__":
    main()