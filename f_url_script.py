#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re

with open("./data/faceScrub/facescrub_actors.txt") as mfile, open("./data/faceScrub/facescrub_actresses.txt") as ffile:
    text1 = mfile.read();
    text2 = ffile.read();

m_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text1)
f_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text2)


# In[2]:


# -*- coding: utf-8 -*-
# for males
import io
import random
import shutil
import sys
from multiprocessing.pool import ThreadPool
import pathlib

import requests
from PIL import Image
import time


start = time.time()

def image_downloader(img_url: str):
    """
    Input:
    param: img_url  str (Image url)
    Tries to download the image url and use name provided in headers. Else it randomly picks a name
    """
    print(f'Downloading: {img_url}')
    try:   
        res = requests.get(img_url, stream=True)
        count = 1
        while res.status_code != 200 and count <= 5:
            res = requests.get(img_url, stream=True)
            print(f'Retry: {count} {img_url}')
            count += 1
        # checking the type for image
        if 'image' not in res.headers.get("content-type", ''):
            print('ERROR: URL doesnot appear to be an image')
            return False
        # Trying to red image name from response headers
        try:
            image_name = str(img_url[(img_url.rfind('/')) + 1:])
            if '?' in image_name:
                image_name = image_name[:image_name.find('?')]
        except:
            image_name = str(random.randint(11111, 99999))+'.jpg'

        i = Image.open(io.BytesIO(res.content))
        download_location = "./data/faceScrubImg/female"
        i.save(download_location + '/'+image_name)
        return f'Download complete: {img_url}'
    except:
        print("error")


def run_downloader(process:int, images_url:list):
    """
    Inputs:
        process: (int) number of process to run
        images_url:(list) list of images url
    """
    print(f'MESSAGE: Running {process} process')
    results = ThreadPool(process).imap_unordered(image_downloader, images_url)
    for r in results:
        print(r)


try:
    num_process = int(sys.argv[2])
except:
    num_process = 10

run_downloader(num_process, f_urls)


end = time.time()
print('Time taken to download {}'.format(len(f_urls)))
print(end - start)


# In[3]:




