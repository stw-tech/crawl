# Web Crawling
This respository shows the code of crawling different websites

# Configuration
compiler: python 3.6  

Using `pip` to install the requested libraries 
## Common Library
- `requests` 
- `bs4`
- `pandas`
- `xlrd`
- `lxml`
- `xmltojson` 
  - should comment out one line in xmltojson.py or it will happen some error, there are an example below 

  ```
  # --- Setup

  import json
  import os
  import sys
  import xmltodict

  # import utils  <- should comment out this line 

  ```
## NCBI Library
- `biopython`
