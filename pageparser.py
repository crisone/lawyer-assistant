from bs4 import BeautifulSoup
import re
import html


def parse_un_page(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    title_spans = soup.find_all("span", id=re.compile("cfTitle"))

    paper_list = []

    for t in title_spans:
        paper = {
            "title": t.get_text(),
            "files": []
        }

        tid = t["id"]
        detail_id = tid.replace("cfTitle", "details1")

        detail_div = soup.find("div", id=detail_id)

        if detail_div == None:
            continue

        detail_docs = detail_div.find_all("a", attrs={"class": "odsDoc"})

        for d in detail_docs:
            doc = {}
            doc["url"] = d["href"]
            lan_div = d.find_previous("span", attrs={"class": "odsTitle"})
            doc["lan"] = lan_div.get_text()
            paper["files"].append(doc)

            sr = re.search(r'[a-zA-Z]+', d["title"])
            if sr != None:
                doc["format"] = sr[0]
            else:
                doc["format"] = "unknown"

        paper_list.append(paper)

    return paper_list


if __name__ == "__main__":
    with open("p3.html") as f:
        content = f.read()

    parse_un_page(content)
