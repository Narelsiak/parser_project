import random
from django.core.files.uploadedfile import UploadedFile

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB limit

def _shuffle_middle(word: str) -> str:
    """
    Shuffle the middle letters of a word, keeping the first and last letters.

    Args:
        word (str): The word to shuffle.
    Returns:
        str: Word with shuffled middle letters.
    """
    if len(word) > 3:
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + ''.join(middle) + word[-1]
    return word

def _process_text(text: str) -> str:
    """
    Shuffle the middle letters of each word while preserving line breaks.

    Args:
        text (str): Input text to process.

    Returns:
        str: Text with shuffled middle letters and original newlines preserved.
    """
    def shuffle_line(line: str) -> str:
        words = line.split(' ')
        return ' '.join(_shuffle_middle(word) for word in words)

    lines = text.splitlines()
    return '\n'.join(shuffle_line(line) for line in lines)

def _is_text_file(uploaded_file: UploadedFile) -> bool:
    """
    Check if the uploaded file is a text file.

    Args:
        uploaded_file (UploadedFile): Uploaded file object.
    Returns:
        bool: True if file is a text file (.txt) and MIME type 'text/*', False otherwise.
    """
    return (
        uploaded_file.content_type.startswith('text/') and
        uploaded_file.name.lower().endswith('.txt')
    )

def process_uploaded_file(uploaded_file: UploadedFile) -> str:
    """
    Safely read and process an uploaded text file.

    Args:
        uploaded_file (UploadedFile): File uploaded by the user.
    Returns:
        str: Processed text with middle letters shuffled in each word.
    Raises:
        ValueError: If the file is not a valid text file, too large, or cannot be decoded.
    """
    # File type check
    if not _is_text_file(uploaded_file):
        raise ValueError("Przesłany plik nie jest plikiem tekstowym (.txt).")
    
    # File size check
    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValueError(f"Plik jest za duży, maksymalny rozmiar: {MAX_FILE_SIZE // (1024*1024)} MB.")
    
    # Read and decode
    try:
        text = uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Nie można odczytać pliku. Upewnij się, że jest to plik tekstowy w formacie UTF-8.")

    return _process_text(text)
