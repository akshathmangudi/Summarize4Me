# This .py file contains the logic for the project structure.

# Importing the basic libraries needed.
import os
from pathlib import Path
import logging

# Setting up the boilerplate for logging info
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# Root folder/Project name
root = "Summarize4Me"

# The files and folders to be created for use.
files = [
    ".github/workflows/.gitkeep",
    f"src/{root}/__init__.py",
    f"src/{root}/components/__init__.py",
    f"src/{root}/utils/__init__.py",
    f"src/{root}/utils/common.py",
    f"src/{root}/logging/__init__.py",
    f"src/{root}/config/__init__.py",
    f"src/{root}/config/configuration.py",
    f"src/{root}/pipeline/__init__.py",
    f"src/{root}/entity/__init__.py",
    f"src/{root}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "app.py",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb"
]

# The logic for file and folder creation.
for file in files:
    file = Path(file)
    filedir, filename = os.path.split(file)

    if filedir != "":
        # Doesn't duplicate a folder with the same name.
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")

    if not os.path.exists(file) or (os.path.getsize(file)):
        with open(file, 'w') as f:
            pass
            logging.info(f"Creating file {file}")

    else:
        logging.info(f"{file} already exists.")




