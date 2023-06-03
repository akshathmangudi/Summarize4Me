import os
from box.exceptions import BoxValueError
import yaml
from Summarize4Me.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
# What is ConfigBox used for?
"""
ConfigBox data types allow to access elements using method syntax, rather 
than using the bracket syntax.  
"""

# Why is a decorator defined on top of every function?
"""
For strict output of the correct data type to be outputted, ensure_annotations must be used.
 
Refer to trials.ipynb for the output differences when ConfigBox and ensure_annotations are used. 
"""

@ensure_annotations
def read_yaml(path_yaml: Path) -> ConfigBox:
    """
    Responsible for reading .yaml extension files and logs the existence
    of yaml files.
    """
    try:
        with open(path_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML File: {path_yaml} loaded")
            return ConfigBox(content)
    except BoxValueError:
        raise BoxValueError("YAML File is empty.")
    except Exception as e:
        raise e


@ensure_annotations
def create_dirs(path_dirs: list, verbose=True):
    """
    Creates list of directories
    """
    for path in path_dirs:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created dir at: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """
    Return the size of a file in kilobytes (kb)
    """

    file_size = round(os.path.getsize(path) / 1024)
    return f"~ {file_size} KB"
