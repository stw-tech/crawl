# GCIS
* Finishing crawling `API 6, 13, 15, 24~28, 31~39, 41~48`  
Referer url: <http://data.gcis.nat.gov.tw/od/rule>
* Finishing crawling directors data with company `核准設立` 
* The `business_item.xlsx` should be included in path `../excel/business_item.xlsx`

## Save Path
The original crawling data will be save into following path
* API Path: `../data/<API_NAME>/<para1>/<para2>/<index.json>`
	* ex: ../data/公司登記資本額查詢/核准設立/1~4999/1~1000.json
	* ex: ../data/(測試)營業項目代碼( I專業、科學及技術服務業 )查公司/管理顧問業/1~1000.json
* Directors Path : `../directors_data/<Business_Accounting_NO>/data.json`
	* ex: ../directors_data/80596002/data.json

## Updating Path
The data will be updated everyday by checking exist crawling data and save into following path 
* Path : `../updating_data/<updating_year>/<updating_day>/<Business_Accounting_NO>/data.json`
	* ex: ../updating_data/2019/1105/12445540/data.json
