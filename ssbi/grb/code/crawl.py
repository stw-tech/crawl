import requests
import json
import time
import os
import random
import datetime

start_page = 1
start_year = 82
end_year = 108
data_dir = "C:\\ssbi\\grb\\data"
date = datetime.datetime.now()

url = 'https://grbdef.stpi.narl.org.tw/searcher'
headers = { 'Referer': 'https://www.grb.gov.tw/search'}
data = {
        'keyword': None,
        'queryType': 'GRB05',
        'planYearSt': None,
        'planYearEn': None,
        'actYearSt': 82,
        'actYearEn': 108,
        'memberKeywordScope': 0,
        'organKeywordScope': 0,
        'nowPage': start_page,
        'rowsPerPage': 100,
        'orderType': 'PLAN_YEAR_DESC',
        'codeWiat1': True,
        'codeWiat2': True,
        'codeWiat3': True   }




def check_update():


    for year in range(end_year, start_year-1, -1):

        current_page = start_page
        json_dir = os.path.join(data_dir, str(year))
        if not os.path.exists('../data/{}/{}{}'.format(year, date.month, date.day)):
            os.makedirs('../data/{}/{}{}'.format(year, date.month, date.day))
        json_list = os.listdir(json_dir)
        id_list = [file.replace('.json', "") for file in json_list]
        data['planYearSt'] = year
        data['planYearEn'] = year

        res = requests.post(url=url, data=data, headers=headers)
        total_pages = res.json()['totalPages']
        new_plan_num = res.json()['totalRows']
        data_plan_num = len(id_list)

        new_id_list, diff_list = [], []
        if new_plan_num > data_plan_num:
            print('>> the {}\'s plans should be updated'.format(year))
            print('>> collecting id of plans in {} year'.format(year))
            while current_page <= total_pages:

                print('>> collecting {}/{} pages'.format(current_page, total_pages))
                data['nowPage'] = current_page
                time.sleep(random.uniform(2, 5))
                res = requests.post(url=url, data=data, headers=headers)
                page_json = res.json()
                for plan in page_json['obj']:
                    new_id_list.append(str(plan['id']))
                current_page += 1
            diff_list = list(set(new_id_list) - set(id_list))
            get_data(diff_list, year)
        else:
            print('>> no need to update {}\'s plans'.format(year))

    print('>> finish update '.format(year))


def get_data(id_list, year):

    print('>> updating {}\'s plans, there are {} plans to update'.format(year, len(id_list)))

    for id in id_list:

        detail_url = url + '/' + id
        time.sleep(random.uniform(1, 2))
        res = requests.post(url=detail_url)
        save_json = json.dumps(res.json(), indent=4, sort_keys=True, ensure_ascii=False)

        with open('../data/{}/{}{}/{}.json'.format(year, date.month, date.day, id), 'w', encoding='utf-8') as f:
            f.write(save_json)


if __name__ == "__main__":

    check_update()