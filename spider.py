import json
import requests
import re
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup

HOME_URL = "https://documents.un.org/prod/ods.nsf/home.xsp"
SEARCH_URL = "https://documents.un.org/prod/ods.nsf/home.xsp"
# SEARCH_URL = "https://documents.un.org/prod/ods.nsf/xpSearchResultsE.xsp"
ORIGIN_URL = "https://documents.un.org"
HOST_URL = "documents.un.org"


class UNSpider:
    def __init__(self):
        self.session = requests.session()
        self.session.headers["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    def init_cookies(self):
        r = self.session.get(HOME_URL, verify=False)
        if r.status_code != 200:
            print("GET HOME PAGE URL FAILED")
            return
        print(self.session.cookies)

        soup = BeautifulSoup(r.content, "html.parser")
        view_id_input = soup.find_all("input", attrs={"name": "$$viewid"})
        # view_id_input = soup.find_all("input")
        self.view_id = view_id_input[0].attrs["value"]
        print(view_id_input)
        print(self.view_id)

    def init_search(self, text):
        m = MultipartEncoder(
            fields={
                "view:_id1:_id2:txtSymbol": "",
                "view:_id1:_id2:rgTrunc": "R",
                "view:_id1:_id2:txtWrds": "",
                "view:_id1:_id2:txtSubj": "",
                "view:_id1:_id2:dtPubDateFrom":  "",
                "view:_id1:_id2:dtPubDateTo": "",
                "view:_id1:_id2:dtRelDateFrom": "",
                "view:_id1:_id2:dtRelDateTo": "",
                "view:_id1:_id2:txtJobNo": "",
                "view:_id1:_id2:txtSess":  "",
                "view:_id1:_id2:txtAgItem":  "",
                "view:_id1:_id2:txtFTSrch": text,
                "view:_id1:_id2:cbType": "FP",
                "view:_id1:_id2:cbSort": "R",
                "view:_id1:_id2:hdnSubj": "",
                "$$viewid": self.view_id,
                "$$xspsubmitid": "view:_id1:_id2:_id130",
                "$$xspexecid": "",
                "$$xspsubmitvalue": "",
                "$$xspsubmitscroll": "0|469",
                "view:_id1": "view:_id1"})

        self.session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.session.headers["Accept-Encoding"] = "gzip, deflate, br"
        self.session.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
        self.session.headers["Referer"] = SEARCH_URL
        self.session.headers["Host"] = HOST_URL
        self.session.headers["Origin"] = ORIGIN_URL
        self.session.headers["Sec-Fetch-Dest"] = "document"
        self.session.headers["Sec-Fetch-Mode"] = "navigate"
        self.session.headers["Sec-Fetch-Site"] = "same-origin"
        self.session.headers["Sec-Fetch-User"] = "?1"
        self.session.headers["Upgrade-Insecure-Requests"] = "1"
        self.session.headers["Cache-Control"] = "max-age=0"

        r = self.session.post(SEARCH_URL, data=m,
                              headers={'Content-Type': m.content_type}, verify=False)
        print(r.status_code)

        with open("page_cache.txt", 'w') as f:
            f.write(str(r.content, encoding="utf-8"))


if __name__ == "__main__":
    s = UNSpider()
    s.init_cookies()
    s.init_search("non-intervention")
