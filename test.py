import os

import image
import extractor


workdir = r'D:\workdir\信息抽取：著作权确认书'
datadir = os.path.join(workdir, 'test')
outpath = os.path.join(workdir, 'test.xlsx')
txt_outpath = os.path.join(workdir, 'test.txt')


# 保存txt
def write_txt(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


# 测试一个jpeg
src1 = os.path.join(datadir, '贺晓鹏.jpeg')
text_bulk = image.get_text_bulk(src1)
# for i in text_bulk:
#     print(i)

# image_bulk = image.get_image_bulk(src1)
# for i in image_bulk:
#     i.show()

text_tot = 'xxxxxxxxx分割线xxxxxxxxx\n'.join(text_bulk)
write_txt(txt_outpath, text_tot)

text2 = text_bulk[2]

print(extractor.get_meta(text2))
print(extractor.get_meta_best_match(text_bulk))