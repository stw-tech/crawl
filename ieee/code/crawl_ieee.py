import requests
import json
import time
import os
import random
from collections import Counter
from bs4 import BeautifulSoup
import re




start_year, end_year = 2015, 2016
start_page = 1
request_url = 'https://ieeexplore.ieee.org/rest/search'
headers = {

    'Cookie': '__gads=ID=33322edc0639140e:T=1568173389:S=ALNI_MYWa5hxhSeK_EOmTlw2cggtdKs1rw; s_ecid=MCMID%7C73845786219960699604182634928166791177; fp=7e273d1309983b9cbf58d29c6c2829df; s_fid=0708DC142F92F9BE-052131E1CDDB7AB1; s_vi=[CS]v1|2EBCF21F852A684F-60000120C00046E6[CE]; cookieconsent_status=dismiss; ipCheck=140.118.207.103; ERIGHTS=n975GditQmRQqFootsslXb4m9eS6HsTA*QJkWGonNM3fzG3ET8EkkdAx3Dx3D-18x2dAVvxxx2BOEgLlh6ZPQtUZbfUAx3Dx3DpgcwIzZeq6N8Me4zGfw03Qx3Dx3D-gdpPDF74rjhVhbSezWo23Ax3Dx3D-hAF6CbSbyWBiTg9Gw04M9Ax3Dx3D; ipList=140.118.207.103; TS01109a32=012f3506236b4a40c7937339d0c7c52076123712bef9572bd141c7e1035a65cf03dc70218e1bca5d41fc6a9d109d7288f1d55ce959af7bb4148c3cd091cf6598a221badcab8ddbf36c275cb1f42f46d9d4fe45ff141d8abb0223557b48b9a28f115f24526c91866aa9f5d730d80b913ef2c06a2d08a370d5cba87011d8c4e1a6074b3a699a7e9040ffc70a4b931aea1af0fe4204ab2e36d88f76dd33fed53e4395117e6c3c57d8bb4d0ecca888709c14c590dd505c; TS01cbcee7=012f3506235268053e6f007c4fdf7a01025e81daf8f9572bd141c7e1035a65cf03dc70218e2961717f7f4f2e7a8a6192a63e5bc87fd79aedf763323613adbec9c50f6578b2544674e637bc7c1e5c49dbc5d990b6591fb6bb37ee8001bf81f3a20d650250ae; AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg=1; AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=1687686476%7CMCIDTS%7C18151%7CMCMID%7C73845786219960699604182634928166791177%7CMCAAMLH-1569048056%7C11%7CMCAAMB-1569048056%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1568450456s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0; s_cc=true; HTML_DocIDs=["7511735"]; JSESSIONID=WBguhz-CmtlLvEciMIAt67K6VgVOSKaABGPUiExsjZ0jwmOIidbM!710087425; WLSESSION=186802828.20480.0000; TS01dcb973=012f35062394e5f58d7a27820ffaccfc0be86689c84098199c7e6f8aabd4a1867707431b4882ce3858e0df408a4ecf09a643153b7f3c7439a9fba575de16a203446541904cbd99e8f6fb900cacabd8401a87dffb79; utag_main=v_id:016d1e6afc9f0003734246a3ff9c03073002b06b00bd0$_sn:10$_ss:0$_st:1568445481054$vapi_domain:ieee.org$ses_id:1568443254673%3Bexp-session$_pn:12%3Bexp-session; s_sq=ieeexplore.dev%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fieeexplore.ieee.org%25252Fsearch%25252Fadvanced%2526link%253DSearch%2526region%253DLayoutWrapper%2526.activitymap%2526.a%2526.c%2526pid%253Dhttps%25253A%25252F%25252Fieeexplore.ieee.org%25252Fsearch%25252Fadvanced%2526oid%253DSearch%2526oidt%253D3%2526ot%253DSUBMIT; xpluserinfo=eyJpc0luc3QiOiJ0cnVlIiwiaW5zdE5hbWUiOiJOYXRpb25hbCBUYWl3YW4gVW5pdiBvZiBTY2llbmNlIGFuZCBUZWNobm9sb2d5IiwicHJvZHVjdHMiOiJFQk9PS1M6MTg3MjoyMDE5fE1JVFA6MjAxMzoyMDEzfE1JVFA6MjAxNjoyMDE4fE1DU1lOVEgxfE1DQ0lTOHxJRUx8TUNDSVM5fE1DQ0lTMTB8TUNDSVMxMXxWREV8Tk9LSUEgQkVMTCBMQUJTfCJ9; seqId=8568; TS01dcb973_26=014082121df9e807766c68cb250d057fc587a68b8403a042929a24a1865ede9ccb3f6323e28706e306582201c6984efe30c178aaab897d858b7e3024a86921e783bb6ae696',
    'Content-Type': 'application/json',    # here if i don't add this term, the response will show 403
    'Referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&matchBoolean=true&queryText=(%22Publication%20Title%22:journal)&highlight=true&returnType=SEARCH&rowsPerPage=100&returnFacets=ALL&ranges=2016_2016_Year',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

payload = {
            "action":"search",
            "matchBoolean":True,
            "queryText":'("Publication Title":journal)',
            "highlight":True,
            'rowsPerPage': "100",
            "ranges": None,
            'pageNumber': start_page,
            "returnFacets":["ALL"],
            "returnType":"SEARCH",
            "newsearch": True,
            "sortType": "newest"
           }
def get_articl_id():


    for year in range(start_year, end_year+1):

        art_num = []
        payload['pageNumber'] = start_page
        payload['ranges'] = ["{}_{}_Year".format(year, year)] # single year

        while True:
            try:
                time.sleep(random.uniform(2, 5))
                res = requests.post(url=request_url, data=json.dumps(payload), headers=headers)
                total_pages = res.json()['totalPages']

            except json.decoder.JSONDecodeError:
                print('decode error')
                continue
            break

        while payload['pageNumber'] <= total_pages:

            while True:
                try:
                    time.sleep(random.uniform(2, 5))
                    res = requests.post(url=request_url, data=json.dumps(payload), headers=headers)
                    res_json = res.json()
                    paper_per_page = len(res_json['records'])
                except (json.decoder.JSONDecodeError, KeyError):
                    print('decode error')
                    continue
                break

            for idx in range(paper_per_page):
                save_dict = {}
                save_dict['authors'] = []
                paper = res_json['records'][idx]
                doc_link = 'https://ieeexplore.ieee.org/document/' + paper['articleNumber']

                time.sleep(random.uniform(2, 5))
                doc_res = requests.get(doc_link)
                html_txt = doc_res.text

                soup = BeautifulSoup(html_txt, 'lxml')
                # print(soup.prettify())

                tag = soup.find_all('script', type="text/javascript", src ='')

                for t in tag  :

                    metadata_format = re.compile(r'global.document.metadata=.*', re.MULTILINE)
                    metadata = re.findall(metadata_format, t.text)
                    metadata = [mt.strip() for mt in metadata]

                    if len(metadata) != 0 :
                        metadata = metadata[0][:-1].replace('global.document.metadata=', '')
                        metadata_dict = json.loads(metadata)
                        save_json(metadata_dict, year)

            payload['pageNumber'] += 1




        repeat = list(set(art_num))
        result = Counter(art_num)
        most_common = result.most_common()

        print('art_num')
        print(len(art_num))
        print('repeat')
        print(len(repeat))
        print('most_common')
        print(most_common)

def save_json(crawl_data, year):

    if 'journal' in payload['queryText']:
        dir_name = 'journal'

    path = os.path.join('../newdata/', dir_name, str(year), crawl_data['articleNumber'])

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)


if __name__ == "__main__":

    get_articl_id()
