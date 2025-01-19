import os
import sys
from pathlib import Path

def read_gitignore(path: Path):
    gitignore_path = Path(".gitignore")
    excluded_files = set()
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            excluded_files = {line.strip() for line in f if line.strip() and not line.startswith("#")}
    return excluded_files

def generate_filetree(project_code: str, path: Path, rel_path="", excluded_files=set()):
    tree_html = "<ul>"
    excluded_files = excluded_files.union({"filetree.html"})
    for item in sorted(path.iterdir()):
        if item.name in excluded_files:
            continue
        item_rel_path = os.path.join(rel_path, item.name)
        if item.is_dir():
            tree_html += f'<li class="folder"><details id="{item_rel_path}" open><summary onclick="toggleDetails(\'{item_rel_path}\'); event.preventDefault();">{item.name}/</summary>'
            tree_html += generate_filetree(project_code, item, item_rel_path, excluded_files)
            tree_html += '</details></li>'
        elif item.is_file():
            tree_html += f'<li class="file"><a href="/{project_code}/{item_rel_path}" onclick="setActiveLink(this); saveActiveLink(\'{project_code}/{item_rel_path}\');">{item.name}</a></li>'
    tree_html += "</ul>"
    return tree_html

def create_html(project_code: str):
    project_path = Path(project_code)
    excluded_files = read_gitignore(project_path)
    content = generate_filetree(project_code, project_path, excluded_files=excluded_files)

    output_path = project_path / "filetree.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_filetree.py <project_code>")
        sys.exit(1)
    project_code = sys.argv[1]
    create_html(project_code)
