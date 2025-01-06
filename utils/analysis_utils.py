import os
from typing import Dict, List
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
from utils.languages import LANGUAGE_DICTIONARY
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Tuple
# Convert lists of file extensions to sets for faster lookup
LANGUAGE_DICTIONARY = {lang: set(exts) for lang, exts in LANGUAGE_DICTIONARY.items()}

def detect_language(file_path: str) -> Optional[Tuple[str, str]]:
    _, extension = os.path.splitext(file_path)

    detected_language = None
    for language, extensions in LANGUAGE_DICTIONARY.items():
        if extension in extensions:
            detected_language = language
            break

    if not detected_language:
        try:
            # Read only the first 1024 bytes of the file
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read(1024)
            lexer = guess_lexer_for_filename(file_path, code)
            detected_language = lexer.name
        except (UnicodeDecodeError, ClassNotFound):
            print(f"Skipping file {file_path} due to decoding error or unknown language.")
            return None, None

    return detected_language, file_path

def analyze_folder(folder_path: str) -> Dict[str, List[str]]:
    """
    Analyzes the folder to categorize files by programming language using a custom dictionary first,
    and then falls back to Pygments if needed.

    Args:
        folder_path (str): Path to the folder to analyze.

    Returns:
        Dict[str, List[str]]: A dictionary mapping languages to file paths.
    """
    language_files = {}
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(detect_language, file_paths))

    for detected_language, file_path in results:
        if detected_language:
            language_files.setdefault(detected_language, []).append(file_path)

    return language_files