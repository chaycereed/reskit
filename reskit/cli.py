import argparse
from pathlib import Path
import textwrap

TEMPLATE_DIR_NAME = "templates"
README_TEMPLATE_NAME = "README_template.md"


def create_project_structure(project_path: Path):
    """
    Create the basic folder structure:
    data/raw, data/processed, notebooks, scripts, results, docs, config
    """
    subdirs = [
        "data/raw",
        "data/processed",
        "notebooks",
        "scripts",
        "results"
        "docs",
        "config",
    ]

    project_path.mkdir(parents=True, exist_ok=True)
    for sub in subdirs:
        (project_path / sub).mkdir(parents=True, exist_ok=True)


def render_readme(project_path: Path, project_name: str, description: str):
    """
    Read the README template and write a filled-in README.md
    """
    # Locate the templates directory relative to this file
    current_dir = Path(__file__).resolve().parent
    template_dir = current_dir / TEMPLATE_DIR_NAME
    template_path = template_dir / README_TEMPLATE_NAME

    template_text = template_path.read_text(encoding="utf-8")

    readme_text = template_text.format(
        project_name=project_name,
        description=description,
    )

    (project_path / "README.md").write_text(readme_text, encoding="utf-8")

def copy_notebook_template(project_path: Path):
    current_dir = Path(__file__).resolve().parent
    template_dir = current_dir / TEMPLATE_DIR_NAME
    notebook_template = template_dir / "analysis_template.ipynb"

    target_path = project_path / "notebooks" / "01_analysis_template.ipynb"
    target_path.write_text(notebook_template.read_text(encoding="utf-8"), encoding="utf-8")

def init_command(args):
    project_name = args.name
    description = args.description or "Short description of the project."

    project_path = Path(project_name)

    if project_path.exists():
        print(f"Error: Directory '{project_name}' already exists.")
        return

    print(f"Creating project at: {project_path}")
    create_project_structure(project_path)
    render_readme(project_path, project_name, description)
    copy_notebook_template(project_path)

    print("Done! Project structure created with README.md.")
    print(f"- data/, notebooks/, scripts/, results/, docs/, config/")
    print(f"- README.md populated with project name and description.")


def main():
    parser = argparse.ArgumentParser(
        prog="reskit",
        description="Reproducibility Kit - Automated setup for folders, notebooks, and READMEs for reproducible research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Example:
              python -m reskit.cli init my_project -d "Example reproducible project"
            """
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # init subcommand
    init_parser = subparsers.add_parser("init", help="Create a new project skeleton.")
    init_parser.add_argument("name", help="Name of the project folder to create.")
    init_parser.add_argument(
        "-d", "--description",
        help="Short description for the project README.",
    )
    init_parser.set_defaults(func=init_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()