"""
Command Line Interface for GitProfile Builder.
Uses Click to provide a rich CLI experience for generating GitHub profile READMEs.
"""

import click
import time
from typing import Optional
from pathlib import Path
from tqdm import tqdm
from gitprofilebuilder import gitprofilebuilder
from gitprofilebuilder.templates import TEMPLATES

@click.group()
def cli():
    """GitProfile Builder - Create awesome GitHub profile READMEs from your resume."""
    pass

@cli.command()
@click.argument('resume_path', type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path))
@click.option(
    '--output', '-o',
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    default=Path('profile_readme.md'),
    help='Output path for the generated README.md file.'
)
@click.option(
    '--template', '-t',
    type=click.Choice(list(TEMPLATES.keys()), case_sensitive=False),
    default='minimal',
    help='Template style to use for the profile.'
)
@click.option(
    '--force', '-f',
    is_flag=True,
    help='Overwrite output file if it already exists.'
)
def generate(
    resume_path: Path,
    output: Path,
    template: str,
    force: bool
) -> None:
    """
    Generate a GitHub profile README from a resume PDF.
    
    RESUME_PATH: Path to your resume PDF file
    """
    try:
        # Check if output file exists
        if output.exists() and not force:
            if not click.confirm(f'{output} already exists. Do you want to overwrite it?'):
                click.echo('Operation cancelled.')
                return
        
        # Initialize progress bar
        steps = ['Loading resume', 'Extracting information', 'Generating profile', 'Saving']
        with tqdm(total=len(steps), desc='Generating GitHub profile', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            for step in steps:
                pbar.set_description(f'Processing: {step}')
                
                # Generate the profile (actual work happens here)
                if step == 'Generating profile':
                    gitprofilebuilder(
                        str(resume_path),
                        str(output),
                        template
                    )
                
                # Simulate progress for other steps
                else:
                    time.sleep(0.5)  # Small delay for visual feedback
                
                pbar.update(1)
        
        click.echo(click.style(
            f'\n✨ Successfully generated GitHub profile at {output} using {template} template!',
            fg='green'
        ))
        
    except Exception as e:
        click.echo(click.style(f'\n❌ Error: {str(e)}', fg='red'), err=True)
        raise click.Abort()

@cli.command()
def templates():
    """List available profile templates."""
    click.echo('\nAvailable templates:')
    for name in TEMPLATES.keys():
        click.echo(f'  • {name}')

def main():
    """Entry point for the CLI application."""
    cli()
