import boto3
import json
import glob
from tqdm import tqdm

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GRB')

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

for ieee_data in tqdm(glob.glob("./data/*/*/*.json")):
    try:
        with open(ieee_data , 'r',encoding = 'utf-8') as reader:
            jf = json.loads(reader.read())
        table.put_item(
        Item={
                "abstractC": _ToNull(jf['abstractC']),
                "abstractE":  _ToNull(jf['abstractE']),
                "excuOrganName":  _ToNull(jf['excuOrganName']),
                "host1NameC":  _ToNull(jf['host1NameC']),
                "hostNameList":  _ToNull(jf['hostNameList']),
                "id":  _ToNull(jf['id']),
                "keyword":  _ToNull(jf['keyword']),
                "keywordC":  _ToNull(jf['keywordC']),
                "keywordE":  _ToNull(jf['keywordE']),
                "pengDesc":  _ToNull(jf['pengDesc']),
                "periodEnym":  _ToNull(jf['periodEnym']),
                "periodStym":  _ToNull(jf['periodStym']),
                "planAmt":  _ToNull(jf['planAmt']),
                "planNo":  _ToString(jf['planNo']),
                "planOrganCode":  _ToNull(jf['planOrganCode']),
                "planOrganName":  _ToNull(jf['planOrganName']),
                "planYear":  _ToNull(jf['planYear']),
                "pnchDesc":  _ToNull(jf['pnchDesc']),
                "projkey":  _ToNull(jf['projkey']),
                "researchAttribute":  _ToNull(jf['researchAttribute']),
                "researchField1":  _ToNull(jf['researchField1']),
                "researchField2":  _ToNull(jf['researchField2']),
                "researchType":  _ToNull(jf['researchType']),
                "title":  _ToNull(jf['title'])
            }
        )
    except:
        print(_ToNull(jf['id']))
