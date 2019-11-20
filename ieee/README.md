# IEEE
Crawling IEEE `conference` and `journal` from 1975-2019 years, and update everyday  
Referer URL: <https://ieeexplore.ieee.org/search/advanced/citation>

## How to Run
go to the directory of python code, you can simply run using this command:
```
python crawl_ieee.py
``` 

## Save Path
The original crawling paper saved into following path 
* Path: `../data/<paper_type>/<year>/<articlenumber>/data.json`
	* ex: ../data/journal/2019/8836640/data.json
	* ex: ../data/conference/2019/8644305/data.json

## Updating Path
The paper will be updated everyday by checking exist crawling paper and save into following path 
* Path: `../updating_data/<updating_year>/<updating_day>/<paper_type>/<year>/<articlenumber>/data.json`
	* ex: ../updating_data/2019/1118/journal/2019/8895748/data.json
	* ex: ../updating_data/2019/1118/conference/2019/8895748/data.json