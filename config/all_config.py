import re
import os
import sys
import csv
import time
import json
import struct
# import docx
import socket
import execjs
import random
import base64
import asyncio
import pymysql
import hashlib
import logging
import asyncio
import demjson3 as demjson
import requests
import datetime
import numpy as np
import pandas as pd
from math import ceil
from lxml import etree
from threading import Timer
from lxml.html import tostring
from selenium import webdriver
from multiprocessing import Pool
from urllib.parse import urljoin
from scrapy.selector import Selector
# from parsel import Selector

sys.path.append('/root/shaohang/single_process/config')

sys.path.append('/root/shaohang/single_process/asyncio_config')
from asyncio_config.manager import Manager
from asyncio_config.manager_redis import ManagerRedis
from asyncio_config.my_Requests import *
from items import *


# import importlib
# module = importlib.import_module('.spider.first_spider', package='single_process')
# print(module.first_spider.name)
