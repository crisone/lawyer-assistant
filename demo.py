# -*- coding: utf-8 -*-

import os
import re
from pageparser import parse_un_page
from spider import UNSpider
import json

# a spider download demo

KEYWORD = "non-intervention"
PAGE_COUNT = 3
OUTPUT_DIR = "./output"

s = UNSpider()
s.init_cookies()

docs = []

print("[*] searching first page")
fp = s.init_search(KEYWORD)
dds = parse_un_page(fp)
docs += dds
print("[*] search first page got {} results".format(len(dds)))

for i in range(2, PAGE_COUNT + 1):
    print("[*] searching page {}".format(i))
    p = s.get_search_page(i)
    dds = parse_un_page(p)
    print("[*] search page {} got {} results".format(i, len(dds)))
    docs += dds

dump_dict = {
    "result": docs
}
# dump json file
json.dump(dump_dict, open("output/search_result.json", "w"), indent=True)


# start downloading, file dowload can be parrelized

# for d in docs:
#     for f in d["files"]:
#         if f["lan"] == "英文":

#             sr = re.search(r'/\w+.\w+\?', f["url"])
#             if sr != None:
#                 file_name = sr[0][1:-1]
#             else:
#                 file_name = "unkownfile.bin"

#             if not os.path.exists(OUTPUT_DIR):
#                 os.mkdir(OUTPUT_DIR)

#             save_file_path = os.path.join(OUTPUT_DIR, file_name)

#             if os.path.exists(save_file_path):
#                 print("file {} already exist".format(save_file_path))
#                 continue

#             print("downloading from {}".format(f["url"]))
#             r = s.download(f["url"])
#             if r.status_code != 200:
#                 print("download failed")
#             else:
#                 with open(save_file_path, 'bw') as f:
#                     f.write(r.content)
#                 print("download success")
