import boto3
import json
import glob
from tqdm import tqdm
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('uspto')
fail =[]
def _ToDateTime(data):
    if(data == ""):
        return None
    else:
        time = datetime.strptime(data, "%d %B %Y")
        return time.strftime('%Y-%m-%d')
def _ToNull(data):
    if(data == ""):
        return None
    else:
        return data
def _ToString(data):
    if(data == None):
        return "Null"
    else:
        return data

for pubmed_data in tqdm(glob.glob("./newdata/*/*/*.json")):
    try:
        with open(pubmed_data , 'r',encoding = 'utf-8') as reader:
            jf = json.loads(reader.read())
        table.put_item(
        Item={
            "title": _ToNull(jf["title"]),
            "Publication_Number": _ToNull(jf["Publication_Number"]),
            "Application_Number": _ToNull(jf["Application_Number"]),
            "filing_date": _ToNull(jf["filing_date"]),
            "Publication_Date": _ToNull(jf["Publication_Date"]),
            "Inventors": _ToNull(jf["Inventors"]),
            "link": _ToNull(jf["link"]),
            "Abstract": _ToNull(jf["Abstract"]),
            "Claims": _ToNull(jf["Claims"])
            }
        )
    except:
        print(pubmed_data)
        fail.append(pubmed_data+'\n')
    
fp = open("fail.txt", "a")
# 將 lines 所有內容寫入到檔案

fp.writelines(fail)
        
# 關閉檔案
fp.close()
