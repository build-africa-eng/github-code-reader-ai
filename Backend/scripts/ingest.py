# scripts/ingest.py
import os
import sys
import shutil
from git import Repo
from pathlib import Path

EXTENSIONS = ['.py', '.js', '.ts', '.md', '.tsx', '.jsx']


def clone_repo(repo_url: str, dest: str = "./repo"):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    print(f"Cloning {repo_url} into {dest}...")
    Repo.clone_from(repo_url, dest)


def gather_files(directory: str):
    code_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if content.strip():
                        code_files.append({
                            "path": filepath,
                            "content": content[:2000]  # trim to 2k chars
                        })
    return code_files


def save_chunks(code_files, out_dir="chunks"):
    os.makedirs(out_dir, exist_ok=True)
    for i, file in enumerate(code_files):
        out_path = os.path.join(out_dir, f"chunk_{i}.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f"# {file['path']}\n\n{file['content']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/ingest.py <github_repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    clone_repo(repo_url)
    code_files = gather_files("./repo")
    save_chunks(code_files)
    print(f"Saved {len(code_files)} code chunks to ./chunks/")
