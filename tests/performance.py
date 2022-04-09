#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is a performance comparision.
@author: Jophy and Wu Tingfeng
@file: performance.py
@time: 17/6/5 21:26

Copyright (c) 2022 Wu Tingfeng
Copyright (c) 2017-2018 Jophy
"""

import time

import tldextract
from fasttld import FastTLDExtract
from tld import get_tld

cases = [
         'jophy.com',
         'www.baidu.com.cn',
         'jo.noexist',
         'https://maps.google.com.ua/a/long/path?query=42',
         '1.1.1.1', 'https://192.168.1.1'
        ]

try:
    range = xrange()
except Exception:
    pass

num_iterations = 1000_000

# fasttld (subdomain=True）start
print("fasttld Include subdomains")
for url in cases:
    t1 = time.time()
    t = FastTLDExtract(exclude_private_suffix=True)
    for i in range(1, num_iterations):
        t.extract(url, subdomain=True)
    print("fasttld on '%s' : %ss" % (url, time.time() - t1))
print("")

# tldextract start
print("tldextract")
for url in cases:
    t1 = time.time()
    for i in range(1, num_iterations):
        tldextract.extract(url)
    print("tldextract on '%s' : %ss" % (url, time.time() - t1))
print("")

# tld start
print("tld")
for url in cases:
    t1 = time.time()
    for i in range(1, num_iterations):
        get_tld(url, fix_protocol=True, fail_silently=True)
    print("tld on '%s' : %ss" % (url, time.time() - t1))
print("")

# fasttld（subdomain=False） start
print("fasttld Exclude subdomains")
for url in cases:
    t1 = time.time()
    t = FastTLDExtract(exclude_private_suffix=True)
    for i in range(1, num_iterations):
        t.extract(url, subdomain=False)
    print("fasttld on '%s' : %ss" % (url, time.time() - t1))
print("")
