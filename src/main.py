"""
Command Line Interface for GitProfile Builder.
Uses Click to provide a rich CLI experience for generating GitHub profile READMEs.
"""

import click
import json
import time
from typing import Optional
from pathlib import Path
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich import print as rprint
from rich.pretty import pprint
from rich.syntax import Syntax
from gitprofilebuilder import gitprofilebuilder
from gitprofilebuilder.templates import TEMPLATES

# Initialize rich console
console = Console()

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
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Show detailed processing information.'
)
def generate(
    resume_path: Path,
    output: Path,
    template: str,
    force: bool,
    verbose: bool,
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
        with tqdm(total=len(steps), desc='Generating GitHub profile', 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}',
                 disable=verbose) as pbar:
            
            for step in steps:
                pbar.set_description(f'Processing: {step}')
                
                # Generate the profile (actual work happens here)
                if step == 'Generating profile':
                    data = gitprofilebuilder(
                        str(resume_path),
                        str(output),
                        template,
                        verbose=True  # Always get data when verbose
                    )
                    
                    # Show intermediate data if verbose
                    if verbose and data:
                        # Show resume text
                        if 'resume_text' in data:
                            console.print("\n[bold bright_green]📄 Resume Text:[/]")
                            syntax = Syntax(
                                data['resume_text'],
                                "text",
                                theme="monokai",
                                line_numbers=True,
                                word_wrap=True
                            )
                            console.print(Panel(syntax))
                        
                        # Show structured data
                        if 'structured_data' in data:
                            console.print("\n[bold bright_green]🔍 Structured Data:[/]")
                            
                            # Create tree structure for nested data
                            root = Tree("📋 Resume Structure")
                            
                            def add_to_tree(data: dict, tree: Tree):
                                for key, value in data.items():
                                    if isinstance(value, dict):
                                        branch = tree.add(f"[bold bright_blue]{key}")
                                        add_to_tree(value, branch)
                                    elif isinstance(value, list):
                                        branch = tree.add(f"[bold bright_blue]{key}")
                                        for item in value:
                                            if isinstance(item, dict):
                                                sub_branch = branch.add("•")
                                                add_to_tree(item, sub_branch)
                                            else:
                                                branch.add(f"[light_green]• {item}")
                                    else:
                                        tree.add(f"[bright_blue]{key}:[/] [light_green]{value}")
                            
                            add_to_tree(data['structured_data'], root)
                            console.print(root)
                            
                            # Also show raw data for inspection
                            console.print("\n[bold bright_green]🔍 Raw Data (for inspection):[/]")
                            pprint(data['structured_data'])
                
                # Simulate progress for other steps
                else:
                    time.sleep(0.5)  # Small delay for visual feedback
                
                if not verbose:
                    pbar.update(1)
        
        console.print(Panel(
            f"[bold bright_green]✨ Successfully generated GitHub profile![/]\n\n"
            f"📝 Output: [bright_blue]{output}[/]\n"
            f"🎨 Template: [bright_blue]{template}[/]",
            title="Success",
            border_style="bright_green"
        ))
        
    except Exception as e:
        console.print(Panel(
            f"[bold bright_red]Error: {str(e)}[/]",
            title="Error",
            border_style="bright_red"
        ))
        raise click.Abort()

@cli.command()
def templates():
    """List available profile templates."""
    console.print("\n[bold]Available templates:[/]")
    for name in TEMPLATES.keys():
        console.print(f"  [bright_green]•[/] [bright_blue]{name}[/]")

def main():
    """Entry point for the CLI application."""
    cli()
