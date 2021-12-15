import os
import pdfplumber
import fitz
from PIL import Image
import cv2
def readable(path):
    _, ext = os.path.splitext(path)
    assert ext == '.pdf'
    try:
        with pdfplumber.open(path) as pdf:
            _ = pdf.chars
            _ = pdf.pages
            read_pdf(path)  # 有可以选中但是读不出的pdf
        return True
    except:
        return False


def read_pdf(path):
    text = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def pdf2img(pdf_path, img_path, zoom_x=3., zoom_y=3., rotation_angle=0):
    pdf = fitz.open(pdf_path)
    page = pdf[0]
    trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
    pm = page.getPixmap(matrix=trans, alpha=False)
    pm.writePNG(img_path)
    IMG_MAX_SIZE = 4096
    #IMG_MIN_SIZE = 15
    #获取png文件大小,保证png不超过4M 百度ocr接口的要求
    file_size = os.stat(img_path).st_size/1024
    while file_size > 4000:
        trans = fitz.Matrix(0.5, 0.5).preRotate(rotation_angle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(img_path)
        file_size = os.stat(img_path).st_size/1024
    #保证分辨率最大边不超过4096，最小边不小于15 百度ocr接口的要求
    #img = cv2.imread(img_path)
    img = Image.open(img_path)
    w,h = img.size

    if w > IMG_MAX_SIZE:
        w_new = IMG_MAX_SIZE
        h_new = round(IMG_MAX_SIZE*h/w)
        out = img.resize((w_new,h_new),Image.ANTIALIAS)
        out.save(img_path)
        
    if h > IMG_MAX_SIZE:
       h_new = IMG_MAX_SIZE
       w_new = round(IMG_MAX_SIZE*w/h)
       out = img.resize((w_new,h_new),Image.ANTIALIAS)
       out.save(img_path)
    pdf.close()


def get_text(path):
    return read_pdf(path)

if __name__ == '__main__':
    pdf_file = 'G:/3.pdf'
    img_path = 'G:/3.png'
    pdf2img(pdf_file,img_path)