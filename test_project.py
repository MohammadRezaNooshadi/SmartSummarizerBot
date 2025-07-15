from project import ltr_language, make_pdf, docx, pdf # type: ignore
import os

def test_ltr_language():
    assert ltr_language("English") is True
    assert ltr_language("Persin") is False


def test_make_pdf():
    txt_dict = {1526 : "Hello, this is a test.",
                1527 : "سلام، این یک تست هست"}
    assert make_pdf(1526, txt_dict) == "Files/1526.pdf"
    assert make_pdf(1527, txt_dict) == False
    os.remove("Files/1526.pdf")

def test_docx():
    assert docx("Files/test_file.docx") == "Hello, this is a test Word document."
def test_pdf():
    assert pdf("Files/test_file.pdf") == "Hello, this is a test Word document."
