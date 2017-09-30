#! /usr/bin/python
# -*- coding: utf8 -*-
import time
from page_parsing import url_list

while True:
    print(url_list.find().count())
    time.sleep(5)