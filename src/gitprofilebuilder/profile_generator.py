from typing import Dict
import json

class GitHubProfileGenerator:
    def __init__(self, resume_data: Dict):
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

def generate_github_profile(resume_data: Dict) -> str:
    """Generate a GitHub profile README from resume data."""
    generator = GitHubProfileGenerator(resume_data)
    return generator.generate_profile()

def main():
    # For testing purposes
    resume_json_path = input("Enter the path to the resume JSON file: ")
    try:
        with open(resume_json_path, 'r') as f:
            resume_data = json.load(f)
        
        profile_content = generate_github_profile(resume_data)
        
        # Save to README.md
        with open('README.md', 'w') as f:
            f.write(profile_content)
            
        print("GitHub profile README.md has been generated successfully!")
        
    except Exception as e:
        print(f"Error generating profile: {str(e)}")

if __name__ == "__main__":
    main() 