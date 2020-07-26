import sys

from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.pdfdevice import PDFDevice, TagExtractor
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer3.cmapdb import CMapDB
from pdfminer3.image import ImageWriter
from pdfminer3.layout import LAParams

from io import StringIO
import logging
import glob
import os
import re
import json


def extract_pdf_content(pdf_path):
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    outfp = StringIO()  # 开始捕捉字节流(outfp)
    laparams = LAParams()
    device = TextConverter(rsrcmgr=rsrcmgr, outfp=outfp,
                           codec=codec, laparams=laparams)
    with open(pdf_path, 'rb') as fp:  # 将pdf文件转换为二进制数据
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)  # 解析pdf的每一页，以二进制数据缓存
    mystr = outfp.getvalue()  # 捕获二进制信息流，以字符串的形式返回
    device.close()
    outfp.close()
    return mystr


def read_country_list(path):
    countries = []
    with open(path) as f:
        ct = json.load(f)

    for c in ct:
        countries.append(c["en_short_name"])
        countries.append(c["nationality"])

    return countries


def find_interest(content, keyword, countries):

    county_re = "|".join(countries)

    ki = 0
    segments = []
    while ki < len(content):
        content = content[ki:]
        ret = re.search(keyword, content, flags=re.I)
        if ret:
            ki = ret.span()[1] + 1
            ei = ret.span()[0]
            # print(ei)
            # print(county_re)
            # print(content[:ei])
            it = re.finditer(county_re, content[:ei], flags=re.I)
            si = None
            for match in it:
                si = match.span()[0]
            if si:
                segments.append(content[si: ki])
            else:
                continue
        else:
            break

    return segments


def make_report(pdf_folder, keyword, country_file):
    c = read_country_list(country_file)

    fd_abs = os.path.abspath(pdf_folder)
    fd_name = fd_abs.split("/")[-1]
    report_path = os.path.join(fd_abs, "..", "{}_report.txt".format(fd_name))

    f = open(report_path, "w")

    for d in os.listdir(pdf_folder):
        if ".pdf" in d:
            s = extract_pdf_content(os.path.join(pdf_folder, d))
            tt = find_interest(s, keyword, c)

            head_line = "\n ================= {} got {} interests =========== \n".format(
                d, len(tt))
            print(head_line)
            f.write(head_line)

            seq = 0
            for t in tt:
                seq += 1
                f.write("\n")
                hl = "---------------[{} / {}] in {}--------------- \n".format(
                    seq, len(tt), d)
                f.write(hl)
                f.write(t)
                f.write("\n")


if __name__ == "__main__":

    # single test
    # s = extract_pdf_content("./output/N6608104.pdf")
    # c = read_country_list("./countries.json")
    # tt = find_interest(s, "non-intervention", c)
    # for t in tt:
    #     print("==================================")
    #     print(t)

    # batch test
    make_report("./output", "non-intervention", "./countries.json")
