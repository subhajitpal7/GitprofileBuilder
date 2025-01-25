"""
Collection of awesome GitHub profile README templates with dynamic elements.
"""

import random
from typing import List, Dict

# Cool ASCII art templates for headers
HEADER_ASCII_ART = [
    """
╔═══╗─────╔╗──────────╔═══╦╗
║╔═╗║─────║║──────────║╔═╗║║
║║─╚╬══╦══╣║╔══╦╗╔╦══╗║║─║║║╔══╦═╗
║║╔═╣╔╗║╔═╣║║╔╗║║║║║═╣║║─║║║║╔╗║╔╗╗
║╚╩═║╚╝║╚═╣╚╣╚╝║╚╝║║═╣║╚═╝║╚╣╚╝║║║║
╚═══╩══╩══╩═╩══╩══╩══╝╚═══╩═╩══╩╝╚╝
""",
    """
██████╗ ██████╗  ██████╗ ███████╗██╗██╗     ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║██║     ██╔════╝
██████╔╝██████╔╝██║   ██║█████╗  ██║██║     █████╗  
██╔═══╝ ██╔══██╗██║   ██║██╔══╝  ██║██║     ██╔══╝  
██║     ██║  ██║╚██████╔╝██║     ██║███████╗███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝
""",
]

# Dynamic greetings with emojis
GREETINGS = [
    "Hi there 👋",
    "Hey, nice to meet you! 🌟",
    "Welcome to my GitHub space! 🚀",
    "Hello, fellow coder! 💻",
    "Greetings, earthling! 👾",
]

# Various section headers with emojis
SECTION_HEADERS = {
    "skills": [
        "🛠️ Tech Arsenal",
        "💪 Skills & Expertise",
        "🔧 Tools of the Trade",
        "⚡ Superpowers",
    ],
    "experience": [
        "💼 Professional Journey",
        "🌱 Growth Story",
        "🚀 Experience",
        "💫 Career Adventures",
    ],
    "education": [
        "🎓 Academic Journey",
        "📚 Education",
        "🧠 Learning Path",
        "📖 Academic Background",
    ],
    "certifications": [
        "🏆 Achievements & Certifications",
        "📜 Certifications",
        "🎯 Professional Milestones",
        "🌟 Badges of Honor",
    ],
    "contact": [
        "📫 Let's Connect",
        "🤝 Get in Touch",
        "💌 Contact Me",
        "🌐 Find Me Online",
    ],
}

# Cool skill badge styles
SKILL_BADGE_STYLES = [
    lambda skill: f"`{skill}`",
    lambda skill: f"![{skill}](https://img.shields.io/badge/-{skill}-blue?style=flat-square)",
    lambda skill: f"<img src='https://img.shields.io/badge/-{skill}-success?style=for-the-badge' alt='{skill}' />",
]

# Profile banners and styles
PROFILE_BANNERS = [
    """
<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=2E97F7&center=true&vCenter=true&width=435&lines=Software+Engineer;Problem+Solver;Continuous+Learner" alt="Typing SVG" />
</div>
""",
    """
<div align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user={github_username}&theme=dark" alt="GitHub Streak" />
</div>
""",
]

# Fun facts and quotes templates
FUN_FACTS = [
    "🌱 Currently learning: {learning}",
    "🔭 Working on: {current_project}",
    "💡 Fun fact: I can code with {beverage} in hand!",
    "⚡ Quick fact: I debug like a detective 🔍",
    "🎯 2024 Goal: Contribute more to Open Source",
]

class ProfileTemplate:
    """Base class for profile templates"""
    
    @staticmethod
    def random_greeting() -> str:
        return random.choice(GREETINGS)
    
    @staticmethod
    def random_section_header(section: str) -> str:
        return random.choice(SECTION_HEADERS.get(section, [f"## {section.title()}"]))
    
    @staticmethod
    def random_skill_style() -> callable:
        return random.choice(SKILL_BADGE_STYLES)
    
    @staticmethod
    def random_banner(github_username: str = "") -> str:
        banner = random.choice(PROFILE_BANNERS)
        return banner.format(github_username=github_username)
    
    @staticmethod
    def random_fun_fact(learning: str = "new things", current_project: str = "awesome projects",
                       beverage: str = "coffee") -> str:
        fact = random.choice(FUN_FACTS)
        return fact.format(learning=learning, current_project=current_project, beverage=beverage)

class ModernTemplate(ProfileTemplate):
    """Modern, clean template with dynamic elements"""
    
    def generate(self, data: Dict) -> str:
        # Start with a random ASCII art header
        content = [random.choice(HEADER_ASCII_ART)]
        
        # Add greeting and name with enhanced tagline
        name = data["personal_info"]["name"]
        enhanced = data.get("enhanced", {})
        tagline = enhanced.get("tagline", "")
        
        content.append(f"\n{self.random_greeting()} I'm {name}")
        if tagline:
            content.append(f"### {tagline}\n")
        
        # Add dynamic banner
        content.append(self.random_banner())
        
        # Add impact statement if available
        if enhanced.get("impact_statement"):
            content.append(f"\n> {enhanced['impact_statement']}\n")
        else:
            content.append(f"\n{data['summary']}\n")
        
        # Add current focus areas
        if enhanced.get("current_focus"):
            content.append("### 🎯 Current Focus")
            for focus in enhanced["current_focus"]:
                content.append(f"- {focus}")
            content.append("")
        
        # Add skills with categories
        if enhanced.get("skill_categories"):
            content.append(f"\n{self.random_section_header('skills')}\n")
            cats = enhanced["skill_categories"]
            for category, skills in cats.get("category_name", {}).items():
                content.append(f"### {category}")
                skill_style = self.random_skill_style()
                skills_str = " ".join(skill_style(skill) for skill in skills)
                content.append(f"{skills_str}\n")
        elif data["skills"]["technical_skills"]:
            content.append(f"\n{self.random_section_header('skills')}\n")
            skill_style = self.random_skill_style()
            skills = " ".join(skill_style(skill) for skill in data["skills"]["technical_skills"])
            content.append(f"{skills}\n")
        
        # Add custom sections from LLM
        if enhanced.get("custom_sections"):
            for section in enhanced["custom_sections"]:
                content.append(f"\n### {section['title']}")
                for point in section["content"]:
                    content.append(f"- {point}")
                content.append("")
        
        # Add experience with collaboration style
        if data["work_experience"]:
            content.append(f"\n{self.random_section_header('experience')}\n")
            if enhanced.get("collaboration_style"):
                content.append(f"> {enhanced['collaboration_style']}\n")
            for job in data["work_experience"]:
                content.append(f"### 🏢 {job['title']} @ {job['company']}")
                content.append(f"*{job['duration']}*\n")
                for resp in job["responsibilities"]:
                    content.append(f"- {resp}")
                content.append("")
        
        # Add education
        if data["education"]:
            content.append(f"\n{self.random_section_header('education')}\n")
            for edu in data["education"]:
                content.append(f"### 🎓 {edu['degree']}")
                content.append(f"*{edu['institution']} - {edu['graduation_year']}*\n")
        
        # Add fun facts
        if enhanced.get("fun_facts"):
            content.append("\n### ⚡ Fun Facts")
            for fact in enhanced["fun_facts"]:
                content.append(f"- {fact}")
            content.append("")
        
        # Add GitHub activity highlights
        if enhanced.get("github_activity_highlights"):
            content.append("\n### 📊 GitHub Highlights")
            for highlight in enhanced["github_activity_highlights"]:
                content.append(f"- {highlight}")
            content.append("")
        
        # Add contact information
        content.append(f"\n{self.random_section_header('contact')}\n")
        info = data["personal_info"]
        if info.get("email"):
            content.append(f"- 📧 Email: {info['email']}")
        if info.get("location"):
            content.append(f"- 📍 Location: {info['location']}")
        
        # Add footer with GitHub stats
        content.append("""
<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username={github_username}&show_icons=true&theme=radical" alt="GitHub Stats" />
</div>
""")
        
        return "\n".join(content)

class MinimalTemplate(ProfileTemplate):
    """Minimal and elegant template"""
    
    def generate(self, data: Dict) -> str:
        content = []
        enhanced = data.get("enhanced", {})
        
        # Header with name and tagline
        name = data["personal_info"]["name"]
        tagline = enhanced.get("tagline", "")
        
        content.append(f"# {self.random_greeting()}, I'm {name}")
        if tagline:
            content.append(f"#### {tagline}")
        
        # Impact statement or summary
        impact = enhanced.get("impact_statement", data["summary"])
        content.append(f"\n> {impact}\n")
        
        # Current focus areas
        if enhanced.get("current_focus"):
            content.append("### Current Focus")
            content.append(" · ".join(f"*{focus}*" for focus in enhanced["current_focus"]))
            content.append("")
        
        # Core skills with expertise levels
        if enhanced.get("skill_categories"):
            content.append("### Expertise")
            for skill, level in enhanced["skill_categories"].get("expertise_levels", {}).items():
                content.append(f"- `{skill}` · {level}")
            content.append("")
        
        # Recent experience with collaboration style
        if data["work_experience"]:
            content.append("### Recent Work")
            if enhanced.get("collaboration_style"):
                content.append(f"*{enhanced['collaboration_style']}*\n")
            for job in data["work_experience"][:2]:
                content.append(f"**{job['title']}** @ {job['company']}")
                content.append(f"_{job['duration']}_\n")
        
        # One interesting fact
        if enhanced.get("fun_facts"):
            content.append(f"\n> {random.choice(enhanced['fun_facts'])}\n")
        
        # Contact
        content.append("### Connect")
        info = data["personal_info"]
        contact_items = []
        if info.get("email"):
            contact_items.append(f"[Email]({info['email']})")
        if info.get("location"):
            contact_items.append(f"Based in {info['location']}")
        content.append(" · ".join(contact_items))
        
        return "\n".join(content)

# Available templates
TEMPLATES = {
    "modern": ModernTemplate(),
    "minimal": MinimalTemplate(),
}

def get_template(template_name: str = "minimal") -> ProfileTemplate:
    """
    Get a specific profile template.
    
    Args:
        template_name (str): Name of the template to use ('minimal' or 'modern'). 
                           Defaults to 'minimal'.
    
    Returns:
        ProfileTemplate: The requested template instance
    
    Raises:
        ValueError: If template_name is not valid
    """
    template_name = template_name.lower()
    if template_name not in TEMPLATES:
        raise ValueError(f"Template '{template_name}' not found. Available templates: {', '.join(TEMPLATES.keys())}")
    return TEMPLATES[template_name]

def get_random_template() -> ProfileTemplate:
    """Get a random profile template."""
    return random.choice(list(TEMPLATES.values()))
