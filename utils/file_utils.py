import os
import zipfile
import tempfile
import shutil

def extract_zip(zip_file_path: str) -> str:
    """
    Extracts a zip file to a temporary directory.

    Args:
        zip_file_path (str): Path to the zip file.

    Returns:
        str: Path to the extracted temporary directory.

    Raises:
        zipfile.BadZipFile: If the file is not a zip or is corrupted.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        return temp_dir
    except zipfile.BadZipFile:
        print("Error: The file is not a zip file or it is corrupted.")
        raise

def cleanup_directory(path: str):
    """
    Removes a directory and all its contents.

    Args:
        path (str): Path to the directory.
    """
    shutil.rmtree(path, ignore_errors=True)