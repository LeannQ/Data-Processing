import pytesseract as ts
from PIL import Image
import numpy as np
import BaiduOCR
import os

def stand_up(obj):
    shape = np.array(obj).shape
    if shape[0] > shape[1]:
        return obj
    else:
        arr = np.array(obj)
        arrnew = arr.transpose([1, 0, 2])
        arrnew = arrnew[:, ::-1, :]
        objnew = Image.fromarray(arrnew)
        return objnew


def cut(obj, box=None):
    if not box:
        box = [0, int(np.array(obj).shape[0] * 0.52), np.array(obj).shape[1], np.array(obj).shape[0]]
    r = obj.crop(box)
    return r


def flip_left_to_right(obj):
    arr = np.array(obj)
    new = arr[:, ::-1, :]
    return Image.fromarray(new)


def rotate_pi(obj):
    return obj.rotate(180)


def get_grey_binary(obj, threshold=100):
    new = obj.convert('L')
    arr = np.array(new)
    arr[arr > threshold] = 255
    arr[arr <= threshold] = 0
    return Image.fromarray(arr)



def tesseract_ocr(obj):
    ts.pytesseract.tesseract_cmd = r'F:/Softwares/Tesseract-OCR/tesseract.exe'
    text = ts.pytesseract.image_to_string(obj, lang='chi_sim')
    return text


def tesseract_ocr_v2(path):
    ts.pytesseract.tesseract_cmd = r'F:/Softwares/Tesseract-OCR/tesseract.exe'
    with Image.open(path) as f:
        obj = stand_up(f)
        obj = cut(obj)
        text = ts.pytesseract.image_to_string(obj, lang='chi_sim')
    return text


def get_text(path, engine='baidu'):
    text = ''
    if engine == 'tesseract':
        text = tesseract_ocr_v2(path)
        # print(text)
    if engine == 'baidu':       
        AssureIMG(path)
        text = BaiduOCR.GetOCR_result(path)

    return text


def get_image_bulk(path):
    bulk = list()
    obj = Image.open(path)
    # raw
    bulk.append(obj)
    bulk.append(get_grey_binary(obj))

    # stand up
    obj_up = stand_up(obj)

    # lower half
    half = cut(obj_up)
    bulk.append(half)
    bulk.append(get_grey_binary(half))

    # upper half
    half = cut(rotate_pi(obj))
    bulk.append(half)
    bulk.append(get_grey_binary(half))

    return bulk

def get_image(path):
    
    obj = Image.open(path)

    return obj
'''
def get_text_bulk(path, engine='tesseract'):
    text_bulk = list()
    bulk = get_image_bulk(path)
    if engine == 'tesseract':
        for i in bulk:
            text_bulk.append(tesseract_ocr(i))

    return text_bulk
'''
def get_size(filename):
    
    size =os.path.getsize(filename)
    return size/1024

def compressImage(src_img,dst_img,mb = 1024,step = 5,quality = 100):

    size = get_size(src_img)
    
    img = Image.open(src_img)
    while size > mb:
        img = Image.open(src_img)
        #img = img.convert('RGB')
        img.save(dst_img,quality = quality)
        if quality -step <0:
            break
        quality -= step
        size = get_size(dst_img)
        
    print('File size:' + str(size))
    
def AssureIMG(img_path):
    
    #确保图片内存大小和分辨率满足百度ocr接口的限制
    #内存大小不超过4M，分辨率最大边不超过4096，最小变不小于15（此次数据不会有特别小的图片，所以没加这个处理）
    IMG_MAX_SIZE = 4096
    #IMG_MIN_SIZE = 15
    file_size = get_size(img_path)
    while file_size > 4096:
        file_size = get_size(img_path)
        #压缩图片
        compressImage(img_path,img_path)
        
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


def img2txt(txt_path, text):
    #把识别出来的结果存成txt
    with open(txt_path,'w',encoding = 'utf-8') as f:
        f.write(text)