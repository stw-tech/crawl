import requests
import json
import time
import os
import random
from bs4 import BeautifulSoup
from utils import b_acc_no

request_url = 'https://findbiz.nat.gov.tw/fts/query/QueryCmpyDetail/queryCmpyDetail.do'
headers = {
    'Referer': 'https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

}
form_data = {
    'banNo': '{id}',
}
def get_directors(acc_num_list):

    idx = 0
    for acc_num in acc_num_list:

        crawl_data = {}
        form_data['banNo'] = acc_num
        time.sleep(random.uniform(1, 3))
        try:
            res = requests.post(url = request_url, data = form_data, headers = headers)
        except requests.exceptions.ConnectionError:
            print('requests.exceptions.ConnectionError --> wait for 1 minute and try connect again')
            time.sleep(60)
            continue

        html_txt = res.text
        soup = BeautifulSoup(html_txt, 'lxml')
        # html = soup.prettify()

        position = [i.text.replace('\n', '').replace('\t', '').replace('\r', '') for i in soup.find_all('td', attrs = {"data-title": "職稱"})]
        name = [i.text.replace('\n', '').replace('\t', '').replace('\r', '') for i in soup.find_all('td', attrs = {"data-title": "姓名"})]
        juristic_person = [i.text.replace('\n', '').replace('\t', '').replace('\r', '') for i in soup.find_all('td', attrs = {"data-title": "所代表法人"})]
        shareholding = [i.text.replace('\n', '').replace('\t', '').replace('\r', '') for i in soup.find_all('td', attrs = {"data-title": "持有股份數"})]
        capital_contribution = [i.text.replace('\n', '').replace('\t', '').replace('\r', '') for i in soup.find_all('td', attrs={"data-title": "出資額"})]

        company_name = soup.find('td', text = '公司名稱').next_sibling.next_sibling.contents[0].replace('\n', '').replace('\t', '').replace('\r', '')
        crawl_data['Company_Name'] = company_name
        crawl_data['Business_Accounting_NO'] = acc_num
        crawl_data['Directors'] = []

        if len(position) != 0 :
            for dir_idx in range(len(position)):

                directors = {}
                directors['Position'] = position[dir_idx]
                directors['Name'] = name[dir_idx]
                directors['Juristic_person'] = juristic_person[dir_idx]
                try :
                    directors['Shareholding'] = shareholding[dir_idx]
                except IndexError:
                    directors['Capital_contribution'] = capital_contribution[dir_idx]

                crawl_data['Directors'].append(directors)
        else:

            crawl_data['Directors'].append('None')
        save_json(crawl_data)
        idx += 1

        print('finish {}/{}' .format(idx, len(acc_num_list)))

def save_json(crawl_data):


    path = os.path.join('../directors_data', crawl_data['Business_Accounting_NO'])

    if not os.path.exists(path):
        os.makedirs(path)

    save_json = json.dumps(crawl_data, indent=4, sort_keys = False, separators = (',', ':'), ensure_ascii=False)
    with open(os.path.join(path, 'data.json'), 'w', encoding='utf-8') as f:

        f.write(save_json)

def check_crawled():

    ck_path = '../directors_data'
    crawled_id = os.listdir(ck_path)
    total_id = b_acc_no

    acc_num_list = list(set(total_id) - set(crawled_id))

    return acc_num_list

if __name__ == "__main__":

    acc_num_list = check_crawled()
    get_directors(acc_num_list)
