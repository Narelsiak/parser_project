from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.uploadedfile import UploadedFile
from .utils import process_uploaded_file

def parse_file(request: HttpRequest) -> HttpResponse:
    """
    Django view to upload and process a text file.
    
    GET: Render the upload form.
    POST: Process the uploaded text file and display the result.
    """
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file: UploadedFile = request.FILES['file']
        try:
            result_text = process_uploaded_file(uploaded_file)
        except ValueError as e:
            return render(request, 'upload.html', {'error': str(e)})

        return render(request, 'result.html', {'result': result_text})

    return render(request, 'upload.html')
