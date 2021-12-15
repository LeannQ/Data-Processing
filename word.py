import win32com.client as wc
import docx


# Convert doc to docx
def doc2docx(doc_path, docx_path):
    word = wc.Dispatch("Word.Application")
    print(doc_path)
    doc = word.Documents.Open(doc_path)
    
    doc.SaveAs(docx_path, 12)
    doc.Close()
    word.Quit()


def get_text(path):
    doc = docx.Document(path)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text
