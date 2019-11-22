import requests
import json
import time
import os
import random
from bs4 import BeautifulSoup
import re
import time


start_year, end_year = 1975, 2019
paper_type = ['journal', 'conference']

start_page = 1
request_url = 'https://ieeexplore.ieee.org/rest/search'

headers = {
    'Cookie':'fp=e9a149feac33eafa3bec7b6d77fd0726; s_ecid=MCMID%7C38485061798561223733907138784163590661; cookieconsent_status=dismiss; s_fid=3C5829A171883BF0-0D3010027F36547B; s_vi=[CS]v1|2EAA7DCA852A33CA-60000121E000ED72[CE]; _ga=GA1.2.122590794.1567684575; WLSESSION=237134476.20480.0000; JSESSIONID=_vobVnK_ooRkIX2hDVjrb3e6BMj3HtgdSq6to--ynFaOvHk_zy2y!-507395020; ipCheck=2001:b011:1004:17ca:e08b:82fe:8acb:d1c1; TS01dcb973=012f350623b1e2ccbe2b0318ee8445fa20c9a6120c954022ac7beb05a507dbe0f3d11e11d268b38515b8418de9519e203348b867dde94e950fb6dd6f526bf30dc5623e248d37059931f2abed7de1eb6569d3d73844; TS01109a32=012f350623ddbcdc70b1c6812b48b78f2fb31e1236954022ac7beb05a507dbe0f3d11e11d268b38515b8418de9519e203348b867ddf50cc96b4f867dedd4afbdd1f31a856c58578ad2a2cdb465f4a0458e85f8b1603604ca4696a86b7447971d64a3988644; AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg=1; s_cc=true; AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=1687686476%7CMCIDTS%7C18124%7CMCMID%7C38485061798561223733907138784163590661%7CMCAID%7CNONE%7CMCOPTOUT-1568128915s%7CNONE%7CMCAAMLH-1568726515%7C11%7CMCAAMB-1568726515%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-18157%7CvVersion%7C3.0.0; TS01dcb973_26=014082121d2c25b3a9e0de68919e0703ccbc104282653bd33c799d3c63741ff605133dc5068f951d9591354f5bc3d4304ea56edfededd51831d6611d1187fbec75af2e725d; s_sq=ieeexplore.prod%3D%2526c.%2526a.%2526activitymap.%2526page%253DAdvanced%252520Search%2526link%253DSearch%2526region%253DadvCommandSearch%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DAdvanced%252520Search%2526pidt%253D1%2526oid%253Dfunctiononclick%252528event%252529%25257Breturnfalse%25257D%2526oidt%253D2%2526ot%253DIMG; utag_main=v_id:016c93f3f2a5000e4d3fbf63d46c03073002b06b00978$_sn:9$_ss:0$_st:1568123588163$vapi_domain:ieee.org$ses_id:1568121714811%3Bexp-session$_pn:6%3Bexp-session',
    'Content-Type': 'application/json',
    'Referer':'https://ieeexplore.ieee.org/rest/search',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

}

payload = {
            "action":"search",
            "searchWithin": ["\"Publication Title\":{}", "\"Publication Year\":{}"],
            "highlight":True,
            'rowsPerPage': 100,
            'pageNumber': start_page,
            "returnFacets":["ALL"],
            "returnType":"SEARCH",
            "newsearch": True,
            "sortType": "newest"
           }

updating_dir = '../updating_data/'
checking_dir = '../data'


proxy_list = ['35.242.174.95:3128', '167.71.182.183:3128', '157.245.4.19:3128']

def crawl_ieee(paper_list, p_type, year):

    '''
    this function crawls the paper in metadata

    Args:
        paper_list: The list of paper id should be crawled
        p_type: conference or journal
        year: year
    '''

    print(">>> crawling {} {} paper".format(year, p_type))
    count = 0
    for id in paper_list:

        doc_link = 'https://ieeexplore.ieee.org/document/' + id

        while True:
            try:
                time.sleep(random.uniform(1, 2))
                proxies = get_proxies()
                doc_res = requests.get(doc_link, proxies = proxies)

            except requests.exceptions.ConnectionError as error:
                print('{}: stop for 20s; proxy ip: {};'.format(error, proxies))
                time.sleep(20)
                continue
            except requests.exceptions.ProxyError:
                print('proxy error: stop for 10s')
                time.sleep(10)
                continue
            break

        html_txt = doc_res.text
        soup = BeautifulSoup(html_txt, 'lxml')
        tag = soup.find_all('script', type="text/javascript", src ='')

        for t in tag  :

            metadata_format = re.compile(r'global.document.metadata=.*', re.MULTILINE)
            metadata = re.findall(metadata_format, t.text)
            metadata = [mt.strip() for mt in metadata]

            if len(metadata) != 0 :

                try:
                    metadata = metadata[0][:-1].replace('global.document.metadata=', '')
                    metadata_dict = json.loads(metadata)
                    if metadata_dict != None:
                        save_json(metadata_dict, p_type, year)
                        count += 1
                    else:
                        print('meta_data is empty')
                except json.decoder.JSONDecodeError:
                    print('metadata decode error')

        print('finishing crawling {}/{}'.format(count, len(paper_list)))


def save_json(crawl_data, p_type, year):

    '''
    this function saves the json

    Args:
        crawl_data: The crawling of IEEE data
        p_type: conference or journal
        year: year
    '''

    year_name = time.strftime("%Y", time.localtime())
    date_name = time.strftime("%m%d", time.localtime())

    path = os.path.join(updating_dir, year_name, date_name, p_type, str(year), crawl_data['articleNumber'])

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'))
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:
        f.write(save_json)

def check_crawled(p_type, year):

    '''
    this function checks the paper crawled or not

    Args:
        p_type: journal or conference
        year: the year of the published papers

    Returns:
        paper_list: the list of papers should be crawled
    '''

    print('>>> checking {} {} paper'.format(year, p_type))
    start_time = time.time()

    payload['pageNumber'] = start_page
    payload['searchWithin'] = ["\"Publication Title\":{}".format(p_type), "\"Publication Year\":{}".format(year)]

    ck_path = os.path.join(checking_dir, p_type, str(year))

    if not os.path.exists(ck_path):
        crawled_paper = []
    else:
        crawled_paper = os.listdir(ck_path)

    if os.path.exists(updating_dir):

        year_dir = os.listdir(updating_dir)
        for y in year_dir:
            y_path = os.path.join(updating_dir, y)

            for date in os.listdir(y_path):
                path = os.path.join(y_path, date, p_type, str(year))
                if os.path.exists(path):
                    id = os.listdir(path)
                    crawled_paper.extend(id)
    while True:
        try:
            proxies = get_proxies()
            res = requests.post(url=request_url, data=json.dumps(payload), headers=headers, proxies = proxies)
            total_num = res.json()['totalRecords']
            total_page = res.json()['totalPages']

            if total_page == (total_num // payload['rowsPerPage'] + 1):
                sort_type = ['newest']
            else:  # the up-limited page number is 1000, so crawls the data by change the order into 'newest' and 'oldest'
                sort_type = ['newest', 'oldest']
                total_page = total_num // payload['rowsPerPage'] // 2 + 1
        except :
            continue
        break


    if len(crawled_paper) < total_num:

        total_paper = []
        for sort in sort_type:
            payload['sortType'] = sort
            payload['pageNumber'] = start_page

            while payload['pageNumber'] <= total_page:

                while True:
                    try:
                        time.sleep(random.uniform(1, 3))
                        proxies = get_proxies()
                        res = requests.post(url=request_url, data=json.dumps(payload), headers=headers, proxies = proxies)
                        res_json = res.json()
                        paper_per_page = len(res_json['records'])
                    except json.decoder.JSONDecodeError :
                        print('json decode error; proxy ip: {}; res status: {} --> stop for 20s'.format(proxies, res.status_code))
                        time.sleep(20)
                        continue
                    except requests.exceptions.ProxyError:
                        print('proxy error, ip: {}; res status: {} --> stop for 10s'.format(proxies, res.status_code))
                        time.sleep(10)
                        continue
                    except requests.exceptions.ChunkedEncodingError:
                        print('Chunked Encoding Error, ip: {} --> stop for 20s'.format(proxies))
                        time.sleep(20)
                        continue
                    except requests.exceptions.SSLError:
                        print('SSLError, ip: {} --> stop for 20s'.format(proxies))
                        time.sleep(20)
                        continue

                    break

                for idx in range(paper_per_page):
                    paper = res_json['records'][idx]
                    paper_id = paper['articleNumber']
                    total_paper.append(paper_id)

                payload['pageNumber'] += 1

        total_paper = list(set(total_paper))
        paper_list = list(set(total_paper) - set(crawled_paper))
        end_time = time.time()
        check_time = end_time - start_time

        print('total num of crawling data :{}, finish crawling: {}, need to be crawled: {}, checking time:{:.0f}h:{:.0f}m'
              .format(len(total_paper), len(crawled_paper), len(paper_list), check_time//3600, (check_time//60)%60))

    else:
        print('Don\'t need to update')
        paper_list = []

    return paper_list

def get_proxies():

    '''
    this function picks the proxy randomly

    Returns:
        proxies: proxy
    '''

    index = random.randint(0, len(proxy_list) - 1)
    proxies = {'https': proxy_list[index]}

    return proxies

if __name__ == "__main__":

    for type in paper_type:

        for year in range(end_year, start_year-1, -1):
            paper_list = check_crawled(type, year)
            if paper_list:
                crawl_ieee(paper_list, type, year)