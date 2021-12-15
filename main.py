import os
import pandas as pd
import tqdm
import extractor
import word
import pdf
import image


# Collect file information
def collect_info(root):
    # r is list of [file name, file name without ext, extension name, file path]
    r = list()
    info = os.walk(root)
    for i in info:
        direc = i[0]
        fs = i[2]
        for f in fs:
            p = os.path.join(direc, f)
            prefix, ext = os.path.splitext(f)
            r.append([f, prefix, ext, p])
    return r


# Save dict-list to excel
def to_excel(path, li):
    columns = li[0].keys()
    df = pd.DataFrame([list(i.values()) for i in li], columns=columns)
    df.to_excel(path, index=False, encoding='utf-8-sig')


def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def run(workdir, datadir, outpath):
    # create tempdir
    tempdir = os.path.join(workdir, 'temp')
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)

    info = collect_info(datadir)

    data = list()
    totnum = len(info)
    for i,item in enumerate(info):
        fname = item[0]
        prefix = item[1]
        ext = item[2]
        path = item[-1]
        print('已完成：{0}；将要处理文件：{1}'.format(str(i+1)+'/'+str(totnum), fname))

        # doc to docx
        if ext == '.doc':
            docx_path = os.path.join(tempdir, fname+'x')
            word.doc2docx(path, docx_path)
            path = docx_path
            ext = '.docx'

        # unreadable pdf to png
        if ext == '.pdf' and not pdf.readable(path):
            img_path = os.path.join(tempdir, prefix+'.png')
            pdf.pdf2img(path, img_path)
            path = img_path
            ext = '.png'

        # get text from file
        text = ''
        if ext == '.docx':
            text = word.get_text(path)
        elif ext == '.pdf':
            text = pdf.get_text(path)
        elif ext.lower() == '.jpg' or ext.lower() == '.png' or ext.lower() == '.jpeg':
            txt_path = os.path.join(tempdir, prefix + '.txt')
            if os.path.exists(txt_path):
                text = read_txt(txt_path)
            else:
                
                text = image.get_text(path)
                image.img2txt(txt_path, text)
            #text = image.get_text_bulk(path)
        else:
            pass

        #get meta data
        meta = extractor.get_meta_best_match(text)
        # 如果是ocr识别的，删掉姓名。因为极其不准确，都是杂讯
        if ext.lower() == '.jpg' or ext.lower() == '.png' or ext.lower() == '.jpeg':
            meta['姓名'] = ''
        meta['filename'] = fname
        meta['filepath'] = path
        data.append(meta)
    
    to_excel(outpath, data)


if __name__ == '__main__':
    
    #workdir = r'G:/ECPH_LY/Data/协助同事/！三版内容中心'
    #datadir = os.path.join(workdir, '6.交叉学科著作权确认书')
    workdir = r'G:/ECPH_LY/Data/协助同事/王红丽/著作权确认书/2012-12-08'
    datadir = os.path.join(workdir, '手工艺')
    outpath = os.path.join(workdir, '著作权信息提取结果-手工艺.xlsx')


    run(workdir, datadir, outpath)
