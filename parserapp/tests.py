import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from parserapp.utils import process_uploaded_file, _shuffle_middle

class UtilsTests(TestCase):
    """
    Unit tests for text file parsing utility functions.
    """

    def test_shuffle_middle_changes_inside(self):
        """
        Ensure that _shuffle_middle() keeps the first and last letter intact
        while shuffling only the middle part of the word.
        """
        word = "python"
        shuffled = _shuffle_middle(word)
        assert shuffled[0] == "p"
        assert shuffled[-1] == "n"
        assert sorted(shuffled) == sorted(word)

    def test_process_uploaded_file_valid_text(self):
        """
        Ensure that process_uploaded_file() correctly processes
        a valid UTF-8 encoded text file.
        """
        content = "Hello world".encode("utf-8")
        file = SimpleUploadedFile("test.txt", content, content_type="text/plain")
        result = process_uploaded_file(file)
        assert isinstance(result, str)
        assert len(result.split()) == 2  # two words expected

    def test_process_uploaded_file_invalid_type(self):
        """
        Ensure that non-text files (e.g., images) raise ValueError.
        """
        file = SimpleUploadedFile("test.jpg", b"not text", content_type="image/jpeg")
        with pytest.raises(ValueError):
            process_uploaded_file(file)

    def test_process_uploaded_file_too_large(self):
        """
        Ensure that oversized files above the MAX_FILE_SIZE limit raise ValueError.
        """
        content = b"a" * (30 * 1024 * 1024)  # 30 MB
        file = SimpleUploadedFile("big.txt", content, content_type="text/plain")
        with pytest.raises(ValueError):
            process_uploaded_file(file)

    def test_process_uploaded_file_invalid_encoding(self):
        """
        Ensure that files with invalid encoding (not UTF-8) raise ValueError.
        """
        bad_bytes = "żółć".encode("cp1250")  # non-UTF8
        file = SimpleUploadedFile("bad.txt", bad_bytes, content_type="text/plain")
        with pytest.raises(ValueError):
            process_uploaded_file(file)

class ParseFileViewTests(TestCase):
    """
    View tests for the parse_file Django view.
    """

    def test_get_request_renders_form(self):
        """
        GET request should render the upload form.
        """
        response = self.client.get(reverse("parse-file"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_post_valid_file(self):
        """
        POST with a valid text file should render the result page
        and include the processed text.
        """
        content = b"Hello test"
        file = SimpleUploadedFile("ok.txt", content, content_type="text/plain")
        response = self.client.post(reverse("parse-file"), {"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "result.html")
        self.assertContains(response, "result")

    def test_post_invalid_file_type(self):
        """
        POST with an invalid file type (e.g., .jpg) should render the upload page
        with an appropriate error message.
        """
        file = SimpleUploadedFile("bad.jpg", b"123", content_type="image/jpeg")
        response = self.client.post(reverse("parse-file"), {"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "upload.html")
        self.assertContains(response, "nie jest plikiem tekstowym")

    def test_post_too_large_file(self):
        """
        POST with a too large file should render the upload page
        with a size limit error message.
        """
        file = SimpleUploadedFile("huge.txt", b"a" * (30 * 1024 * 1024), content_type="text/plain")
        response = self.client.post(reverse("parse-file"), {"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Plik jest za duży")