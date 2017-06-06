#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is a performance comparision.
@author: Jophy
@file: performance.py
@time: 17/6/5 21:26

Copyright (c) 2017 Jophy
"""

import time

from fasttld import FastTLDExtract
from tld import get_tld
import tldextract

case1 = 'jophy.com'
case2 = 'www.baidu.com.cn'
case3 = 'jo.noexist'

try:
    range = xrange()
except:
    pass

# fasttld start
t1 = time.time()
t = FastTLDExtract(exclude_private_suffix=False)
for i in range(1, 1000000):
    t.extract(case1, subdomain=True)
print("fasttld in case1: %ss" % (time.time() - t1))

t1 = time.time()
t = FastTLDExtract(exclude_private_suffix=False)
for i in range(1, 1000000):
    t.extract(case2, subdomain=True)
print("fasttld in case2: %ss" % (time.time() - t1))

t1 = time.time()
t = FastTLDExtract(exclude_private_suffix=False)
for i in range(1, 1000000):
    t.extract(case3, subdomain=True)
print("fasttld in case3: %ss\n" % (time.time() - t1))

# fasttld（subdomain=False） start
t1 = time.time()
t = FastTLDExtract(exclude_private_suffix=False)
for i in range(1, 1000000):
    t.extract(case1, subdomain=False)
print("fasttld in case1: %ss" % (time.time() - t1))

t1 = time.time()
t = FastTLDExtract(exclude_private_suffix=False)
for i in range(1, 1000000):
    t.extract(case2, subdomain=False)
print("fasttld in case2: %ss" % (time.time() - t1))

t1 = time.time()
t = FastTLDExtract(exclude_private_suffix=False)
for i in range(1, 1000000):
    t.extract(case3, subdomain=False)
print("fasttld in case3: %ss\n" % (time.time() - t1))


# tldextract start
t1 = time.time()
for i in range(1, 1000000):
    tldextract.extract(case1)
print("tldextract in case1: %ss" % (time.time() - t1))

t1 = time.time()
for i in range(1, 1000000):
    tldextract.extract(case2)
print("tldextract in case2: %ss" % (time.time() - t1))

t1 = time.time()
for i in range(1, 1000000):
    tldextract.extract(case3)
print("tldextract in case3: %ss\n" % (time.time() - t1))

# tld start
t1 = time.time()
for i in range(1, 1000000):
    get_tld(case1, fix_protocol=True)
print("tld in case1: %ss" % (time.time() - t1))

t1 = time.time()
for i in range(1, 1000000):
    get_tld(case1, fix_protocol=True)
print("tld in case2: %ss" % (time.time() - t1))

t1 = time.time()
for i in range(1, 1000000):
    get_tld(case1, fix_protocol=True)
print("tld in case3: %ss\n" % (time.time() - t1))