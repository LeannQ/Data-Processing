1.本项目从多种格式的著作权确认书电子版抽取所需信息。

2.接受数据格式包括doc、docx、可读pdf、不可读pdf、jpg、jpeg。

3.读取doc的过程迂回了一下，用win32com调用office客户端，将doc转为了临时docx文件。

4.图像识别采用tesseract，用pytesseract调用。