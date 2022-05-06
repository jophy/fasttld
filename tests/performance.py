#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Performance comparison with similar modules
@author: Jophy and Wu Tingfeng
@file: performance.py

Copyright (c) 2022 Wu Tingfeng
Copyright (c) 2017-2018 Jophy
"""

import sys
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

if sys.version_info.major == 2:
    range = xrange  # type: ignore

num_iterations = 10000000

t = FastTLDExtract(exclude_private_suffix=True)

test_cases = [('fasttld_with_subdomains',
              t.extract,
              {'subdomain': True}),
              ('tldextract',
               tldextract.extract,
              {}),
              ('tld',
              get_tld,
              {'fix_protocol': True, 'fail_silently': True}),
              ('fasttld_without_subdomains',
               t.extract,
              {'subdomain': False})
              ]

for test_case in test_cases:
    module, extractor, kwargs = test_case
    for url in cases:
        t1 = time.perf_counter()
        for i in range(1, num_iterations):
            extractor(url, **kwargs)  # type: ignore
        print("%s on '%s' : %.2fs" % (module, url, time.perf_counter() - t1))
    print("")
