# GitHub Profile Builder 🚀

An intelligent tool that generates beautiful GitHub profile READMEs from your resume using AI. Transform your professional experience into an engaging GitHub profile with just one command!

## Features ✨

- **Resume Parsing**: Automatically extracts information from PDF resumes
- **AI-Powered**: Uses Google's Gemini Pro to structure and enhance your profile
- **Multiple Templates**: Choose from different templates:
  - Minimal: Clean and simple layout
  - Modern: Feature-rich layout with badges and GitHub stats
- **Customizable**: Easy to add new templates using Jinja2
- **Smart Enhancement**: Automatically adds:
  - Engaging taglines
  - Impact statements
  - Skill categorization
  - GitHub activity highlights
  - Custom sections with emojis

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/subhajitpal7/GitprofileBuilder.git
cd GitprofileBuilder
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage 💻

### Python API

You can use GitProfile Builder directly in your Python code:

```python
from gitprofilebuilder import generate_and_save_readme

# Basic usage with defaults
generate_and_save_readme(
    resume_path="resume.pdf"  # Will use minimal template and save as profile_readme.md
)

# Advanced usage with all options
result = generate_and_save_readme(
    resume_path="resume.pdf",
    output_path="custom_profile.md",
    template_name="modern",
    verbose=True  # Returns processing data when True
)

if result:  # Only available when verbose=True
    print("Resume Text:", result['resume_text'])
    print("Structured Data:", result['structured_data'])
    print("Enhanced Data:", result['enhanced'])
```

For lower-level control, you can use the ProfileGenerator class:

```python
from gitprofilebuilder import ProfileGenerator

# Initialize the generator
generator = ProfileGenerator(verbose=True)

# Step by step generation
resume_text = generator.extract_resume_text("resume.pdf")
structured_data = generator.extract_structured_data()
enhanced_data = generator.enhance_profile_data()

# Or generate everything at once
profile_data = generator.generate_profile("resume.pdf")
```

### Command Line Interface

The tool provides a rich command-line interface with the following commands:

```bash
# Generate a profile README from your resume
gitprofilebuilder generate RESUME_PATH [OPTIONS]

# List available templates
gitprofilebuilder templates
```

### Generate Command Options

```bash
Options:
  -o, --output PATH     Output path for the generated README.md file [default: profile_readme.md]
  -t, --template TEXT   Template style to use for the profile [default: minimal]
  -f, --force          Overwrite output file if it already exists
  -v, --verbose        Show detailed processing information
  --help              Show this message and exit
```

### Examples

Generate with default options:
```bash
gitprofilebuilder generate resume.pdf
```

Use modern template with custom output:
```bash
gitprofilebuilder generate resume.pdf -t modern -o github_profile.md
```

Force overwrite existing file with verbose output:
```bash
gitprofilebuilder generate resume.pdf -f -v
```

View available templates:
```bash
gitprofilebuilder templates
```

## Templates 🎨

### Available Templates

1. **Minimal** (`minimal.md.j2`)
   - Clean and simple layout
   - Focus on essential information
   - Perfect for minimalists

2. **Modern** (`modern.md.j2`)
   - Rich feature set
   - GitHub stats integration
   - Skill badges
   - Activity graphs

### Creating Custom Templates

1. Add your template to `src/gitprofilebuilder/templates/`
2. Use Jinja2 syntax
3. Available variables:
   - `personal_info`: Name, email, location
   - `summary`: Professional summary
   - `skills`: Technical and soft skills
   - `work_experience`: Work history
   - `education`: Educational background
   - `enhanced`: AI-generated enhancements

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
