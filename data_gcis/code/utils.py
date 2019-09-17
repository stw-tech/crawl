import pandas as pd
import os
import json



b_item_excel = "../excel/business_item.xlsx"

def map_name(key, para_idx):

    if key == 'Business_Current_Status':

        business_status = ['核准設立', '停業', '歇業,撤銷', '申覆(辯)期', '遷他縣市', '列入廢止中', '廢止', '破產', '設立無效']
        index = int(para_idx[key]) - 1
        return business_status[index]

    if key == 'Business_Register_Funds':

        items = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        fund_range = ['1~4999', '5000~9999', '10000~99999', '100000~999999', '1000000~9999999',
                           '10000000~99999999', '100000000以上']
        index = items.index(para_idx[key])
        return fund_range[index]

    if key == 'Company_Status':

        company_status = ['核准設立', '核准設立，但以命令解散', '重整', '解散', '撤銷', '破產', '合併解散', '撤回認許', '廢止', '廢止認許', '解散已清算完結',
                          '撤銷已清算完結', '廢止已清算完結', '撤回認許已清算完結', '撤銷認許已清算完結', '廢止認許已清算完結', '撤銷認許', '分割解散', '終止破產',
                          '中止破產', '塗銷破產','破產程序終結(終止)', '破產程序終結(終止)清算中', '破產已清算完結', '接管', '撤銷無需清算', '撤銷許可', '廢止許可',
                          '撤銷許可已清算完結', '廢止許可已清算完結', '清理', '撤銷公司設立', '清理完結']
        index = int(para_idx[key]) - 1
        return company_status[index]

    if key == 'Capital_Stock_Amount':

        items = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        stock_amount = ['1~4999', '5000~9999', '10000~99999', '100000~999999', '1000000~9999999',
                      '10000000~99999999', '100000000以上']
        index = items.index(para_idx[key])
        return stock_amount[index]

    # if key == 'Business_Item_A':
    #
    #     items = b_code['A']
    #     business_item = b_item['A']
    #     index = items.index(para_idx[key])
    #     return business_item[index]

    item_class = "ABCDEFGHIJZ"
    for cls in item_class:
        if key == 'Business_Item_{}'.format(cls) :
            items = b_code['{}'.format(cls)]
            business_item = b_item['{}'.format(cls)]
            index = items.index(para_idx[key])
            return business_item[index]

    if key == 'Business_Item':

        items = b_code['ALL']
        business_item = b_item['ALL']
        index = items.index(para_idx[key])
        return business_item[index]

    if key == 'Business_Accounting_NO':

        business_accounting_NO = b_acc_no
        name = company_name
        index = business_accounting_NO.index(para_idx[key])

        return name[index]



def get_busisness_item(path):

    data = pd.read_excel(path)
    item_code = data['營業項目代碼']
    item_name = list(data['營業項目'])

    business_code = {}
    business_item = {}
    item_class = "ABCDEFGHIJZ"

    business_code['ALL'] = list(item_code)
    business_item['ALL'] = item_name

    for cls in item_class:
        business_code[cls] = []
        business_item[cls] = []

    idx = 0
    for code in item_code:
        for cls in item_class:
            if code[0] == cls:
                business_code[cls].append(code)
                business_item[cls].append(item_name[idx])
                idx += 1

    return business_code, business_item

def get_business_acc_num():

    api_dir = "../new_data/公司登記資本額查詢"
    status = os.listdir(api_dir)

    business_accounting_NO = []
    company_name = []
    # count = {}

    for dir in status:

        # count[dir] = {}
        if dir == "核准設立":
            status_path = os.path.join(api_dir, dir)
            stock_amount = os.listdir(status_path)
            for amount in stock_amount:

                # count[amount] = []
                stock_amount_dir = os.path.join(status_path, amount)
                json_file = os.listdir(stock_amount_dir)

                for file in json_file:
                    json_path = os.path.join(stock_amount_dir, file)

                    with open(json_path, 'r', encoding = 'utf-8') as f:
                        json_list = json.loads(f.read())

                        for company in json_list :

                            b_acc_no = company['Business_Accounting_NO']
                            name = company['Company_Name']

                            business_accounting_NO.append(b_acc_no)
                            company_name.append(name)
                # count[amount].append(len(business_accounting_NO))
            # print(count)
    return business_accounting_NO, company_name

b_acc_no, company_name = get_business_acc_num()
b_code, b_item = get_busisness_item(b_item_excel)


