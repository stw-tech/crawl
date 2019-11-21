# USPTO
Crawling USPTO data from 2001-2019 years, and update everyday  
Referer URL: <http://appft.uspto.gov/netahtml/PTO/help/helpflds.html#Publication_Date>  
Referer URL: <http://appft.uspto.gov/netahtml/PTO/search-adv.html>  

`new_crawl_uspto.py` add the `Kind Code`, `Assignee`, `PCT Filed`, `PCT NO`, `Description` columns for next year schedule

## How to Run
go to the directory of python code, you can simply run using this command:
```
python crawl_uspto.py
``` 

## Save Path
The original crawling patents will be save into following path
* Path: `../data/<year>/<Publication_Number>/data.json`
	* ex: ../data/2018/20180000002/data.json

* New Path: `../newdata/<year>/<Publication_Number>/data.json`
	* ex: ../newdata/2018/20180000002/data.json

## Updating Path 
The patents will be updated everyday by checking exist crawling patents and save into following path 
* Path: `../updating_data/<updating_year>/<updating_day>/<PY+year>/<Publication_Number>/data.json`
	* ex: ../updating_data/2019/1105/PY2018/20180000002/data.json

