from django.core.files.uploadedfile import UploadedFile

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB limit

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

    return text
