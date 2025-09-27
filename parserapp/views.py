from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.uploadedfile import UploadedFile

def parse_file(request: HttpRequest) -> HttpResponse:
    return render(request, 'upload.html')
