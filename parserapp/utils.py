from django.core.files.uploadedfile import UploadedFile

def process_uploaded_file(uploaded_file: UploadedFile) -> str:
    try:
        text = uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Nie można odczytać pliku. Upewnij się, że jest to plik tekstowy w formacie UTF-8.")

    return text
