import json
import requests
import re
from requests_toolbelt import MultipartEncoder
from urllib.parse import urlencode, quote
from bs4 import BeautifulSoup

HOME_URL = "https://documents.un.org/prod/ods.nsf/home.xsp"
INIT_SEARCH_URL = "https://documents.un.org/prod/ods.nsf/home.xsp"
SEARCH_URL = "https://documents.un.org/prod/ods.nsf/xpSearchResultsE.xsp"
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
        print("first viewid: " + self.view_id)

    def init_search(self, text):
        self.form_fields = {
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
            "view:_id1": "view:_id1"
        }

        m = MultipartEncoder(fields=self.form_fields)

        self.session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.session.headers["Accept-Encoding"] = "gzip, deflate, br"
        self.session.headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
        self.session.headers["Referer"] = INIT_SEARCH_URL
        self.session.headers["Host"] = HOST_URL
        self.session.headers["Origin"] = ORIGIN_URL
        self.session.headers["Sec-Fetch-Dest"] = "document"
        self.session.headers["Sec-Fetch-Mode"] = "navigate"
        self.session.headers["Sec-Fetch-Site"] = "same-origin"
        self.session.headers["Sec-Fetch-User"] = "?1"
        self.session.headers["Upgrade-Insecure-Requests"] = "1"
        self.session.headers["Cache-Control"] = "max-age=0"

        r = self.session.post(INIT_SEARCH_URL, data=m,
                              headers={'Content-Type': m.content_type}, verify=False)
        print(r.status_code)

        if r.status_code == 200:
            print("init search success")
            soup = BeautifulSoup(r.content, "html.parser")
            view_id_input = soup.find_all("input", attrs={"name": "$$viewid"})
            self.view_id = view_id_input[0].attrs["value"]
            self.form_fields["$$viewid"] = self.view_id
            print("new viewid: " + self.view_id)

        return str(r.content, encoding="utf-8")

    def get_search_page(self, page_no):
        self.form_fields["$$xspsubmitid"] = "view:_id1:_id2:cbMain:_id135:pager1__Group__lnk__{}".format(
            page_no - 1)
        self.form_fields["$$xspexecid"] = "view:_id1:_id2:cbMain:_id135:pager1"
        self.form_fields["$$xspsubmitscroll"] = "0|334"
        self.form_fields["view:_id1:_id2:cbLang"] = ""

        data = urlencode(self.form_fields)
        data = data.replace("%21", "!")

        self.session.headers["Referer"] = INIT_SEARCH_URL
        self.session.headers["Sec-Fetch-Dest"] = "empty"
        self.session.headers["Sec-Fetch-Mode"] = "cors"
        self.session.headers["Sec-Fetch-Site"] = "same-origin"
        self.session.headers["X-Requested-With"] = "XMLHttpRequest"

        url = SEARCH_URL + "?$$ajaxid=view%3A_id1%3A_id2%3AcbMain%3AmainPanel"

        r = self.session.post(url, data=data,
                              headers={'Content-Type': "application/x-www-form-urlencoded"}, verify=False)

        if r.status_code == 200:
            print("search page success")
        else:
            print("search page failed, status code {}".format(r.status_code))

        return str(r.content, encoding="utf-8")

    def download(self, doc_link):

        headers = {
            "Host": "documents-dds-ny.un.org",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

        r = self.session.get(doc_link, headers=headers, verify=False)
        return r


if __name__ == "__main__":
    s = UNSpider()
    s.init_cookies()
    fp = s.init_search("non-intervention")
    with open("p_first.html", "w") as f:
        f.write(fp)
    p3 = s.get_search_page(3)
    with open("p3.html", "w") as f:
        f.write(p3)
