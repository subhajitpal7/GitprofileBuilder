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

## Installation 🚀

### Using pip

```bash
# Install the latest stable version
pip install gitprofilebuilder

# Or install from TestPyPI (for pre-release versions)
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gitprofilebuilder
```

### Prerequisites
- Python 3.11+
- A Google AI API key (for AI-powered resume processing)

### Setting Up API Key

1. Get a Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the API key as an environment variable:

```bash
# For Linux/macOS
export GOOGLE_API_KEY='your_api_key_here'

# For Windows (PowerShell)
$env:GOOGLE_API_KEY='your_api_key_here'
```

Or create a `.env` file in your project directory:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage 💻

### CLI Usage

```bash
# Generate GitHub profile README
gitprofile /path/to/resume.pdf

# Specify output file and template
gitprofile /path/to/resume.pdf -o my_profile.md -t modern

# Show verbose output
gitprofile /path/to/resume.pdf -v
```

### Options
- `-o, --output`: Specify output file path (default: `profile_readme.md`)
- `-t, --template`: Choose template style (default: `minimal`)
- `-f, --force`: Overwrite existing output file
- `-v, --verbose`: Show detailed processing information

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

### Examples

Generate with default options:
```bash
gitprofile generate resume.pdf
```

Use modern template with custom output:
```bash
gitprofile generate resume.pdf -t modern -o github_profile.md
```

Force overwrite existing file with verbose output:
```bash
gitprofile generate resume.pdf -f -v
```

View available templates:
```bash
gitprofile templates
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
