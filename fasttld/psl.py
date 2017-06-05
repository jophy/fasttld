#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jophy
@file: psl.py
@time: 17/5/29 00:09

Copyright (c) 2017 Jophy
"""
import urllib
import os.path
import time


def getPublicSuffixList(file_path):
    """
    Get a suffix list with none private suffix list. (eg, blogspot.com)
    :return: Tuple()
    PublicSuffixList: The common domain suffix. Eg, com,net,org
    PrivateSuffixList: The suffixes including Private domains. Eg, blogspot.co.uk
    AllSuffixList: Including all suffix lists above.
    """
    PublicSuffixList = list()
    PrivateSuffixList = list()
    AllSuffixList = list()
    pri_flag = False
    if not file_path:
        file_path = os.path.dirname(os.path.realpath(__file__)) + '/public_suffix_list.dat'

    if not os.path.isfile(file_path):
        raise Exception("\rPath:" + file_path + " .\nPublic suffix list file not found.")

    with open(file_path, 'r') as fd:
        for line in fd:
            line = line.strip()
            if "// ===BEGIN PRIVATE DOMAINS===" == line:
                pri_flag = True
            if line == "":
                continue
            if line.startswith("//"):
                continue
            if pri_flag:
                PrivateSuffixList.append(line.decode('utf-8').encode('idna'))
            else:
                PublicSuffixList.append(line.decode('utf-8').encode('idna'))
            AllSuffixList.append(line.decode('utf-8').encode('idna'))
    return PublicSuffixList, PrivateSuffixList, AllSuffixList


def update():
    """
    Update Public Suffix List from https://publicsuffix.org/list/public_suffix_list.dat 
    :return: 
    """
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/public_suffix_list.dat"
    base_url = 'https://publicsuffix.org/list/public_suffix_list.dat'
    downfile = urllib.URLopener()
    downfile.retrieve(base_url, file_path)


def auto_update():
    """
    Update Public Suffix List from https://publicsuffix.org/list/public_suffix_list.dat
    This function will update public_suffix_list.dat file every 3 days.
    :return: 
    """
    need_update = False
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/public_suffix_list.dat"
    if os.path.isfile(file_path):
        # updates in 3 days
        if (time.time() - os.path.getmtime(file_path))/3600/24 > 3:
            need_update = True
    else:
        # file not found
        need_update = True
    if need_update:
        update()

auto_update()
