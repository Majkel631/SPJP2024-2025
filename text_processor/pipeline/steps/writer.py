import os

def write_file(path, content, overwrite=False):
    if not overwrite and os.path.exists(path):
        raise FileExistsError(f"File already exists: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
