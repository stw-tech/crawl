# Web Crawling
This respository shows the code of crawling different websites

# Configuration
compilerpython 3.6  
Using `pip` to install the requested libraries 
- `requests` 
- `bs4`
- `pandas`
- `xlrd`
- `lxml` 
- `biopython`
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
