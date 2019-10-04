import boto3
import json


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GRB')


with open('./grb/example.json' , 'r',encoding = 'utf-8') as reader:
    jf = json.loads(reader.read())


table.put_item(
   Item={
        "abstractC": jf['abstractC'],
        "abstractE": jf['abstractE'],
        "excuOrganName": jf['excuOrganName'],
        "host1NameC": jf['host1NameC'],
        "hostNameList": jf['hostNameList'],
        "id": jf['id'],
        "keyword": jf['keyword'],
        "keywordC": jf['keywordC'],
        "keywordE": jf['keywordE'],
        "pengDesc": jf['pengDesc'],
        "periodEnym": jf['periodEnym'],
        "periodStym": jf['periodStym'],
        "planAmt": jf['planAmt'],
        "planNo": jf['planNo'],
        "planOrganCode": jf['planOrganCode'],
        "planOrganName": jf['planOrganName'],
        "planYear": jf['planYear'],
        "pnchDesc": jf['pnchDesc'],
        "projkey": jf['projkey'],
        "researchAttribute": jf['researchAttribute'],
        "researchField1": jf['researchField1'],
        "researchField2": jf['researchField2'],
        "researchType": jf['researchType'],
        "title": jf['title']
    }
)