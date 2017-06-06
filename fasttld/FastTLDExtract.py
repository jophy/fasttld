#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jophy
@file: psl.py
@time: 17/5/28 23:36

Copyright (c) 2017 Jophy
"""
from fasttld.psl import getPublicSuffixList
from fasttld.psl import update

import idna


class FastTLDExtract(object):
    def __init__(self, exclude_private_suffix=False, file_path=''):
        self.trie = self._trie_construct(exclude_private_suffix, file_path)

    def update(self):
        update()

    def nested_dict(self, dic, keys):
        """
        The idea of this function is based on https://stackoverflow.com/questions/13687924
        :param dic: 
        :param keys: 
        :return: 
        """
        for key in keys[:-1]:
            dic_bk = dic
            dic = dic.setdefault(key, {})
            if isinstance(dic, bool):
                dic = dic_bk
                dic[keys[-2]] = {}
                dic[keys[-2]].update({
                    '_END': True,
                    keys[-1]: True
                })
        dic[keys[-1]] = True

    def _trie_construct(self, exclude_private_suffix, file_path=''):
        """
        This function for building a trie structure based on Mozilla Public Suffix List.
        In order to construct this, all suffixes sorted in a reverse order.
        For example, www.google.com -> com.google.www
        :return: a trie dict
        """
        tld_trie = {}
        PublicSuffixList, PrivateSuffixList, AllSuffixList = getPublicSuffixList(file_path)
        if exclude_private_suffix:
            SuffixList = PublicSuffixList
        else:
            SuffixList = AllSuffixList
        for suffix in SuffixList:
            if '.' in suffix:
                sp = suffix.split('.')
                sp.reverse()
                self.nested_dict(tld_trie, sp)
            else:
                tld_trie.update({
                    suffix: {
                        '_END': True
                    }
                })
        for key, val in tld_trie.items():
            if len(tld_trie[key]) == 1:
                if '_END' in val:
                    tld_trie.update({
                        key: True
                    })
        return tld_trie

    def extract(self, input, subdomain=True, format=False):
        """
        Extract suffix and subdomain from a Domain.
        :param input: 
        :param subdomain: Output options. This option will reduce efficiency. Maybe 10% 
        :param format: To format input string.
        :return: Tuple(subdomain, domain, suffix, domain_name)
        >>> FastTLDExtract.extract('www.google.com.hk', subdomain=True)
        >>> ('www', 'google', 'com.hk', 'google.com.hk')
        """
        ret_subdomain = ''
        ret_domain = ''
        ret_suffix = ''
        ret_domain_name = ''
        if format:
            input = self.format(input)
        labels = input.split('.')
        labels.reverse()
        node = self.trie  # define the root node
        suffix = []

        for index, label in enumerate(labels):
            if node is True:
                # This node is an end node.
                ret_domain = label
                break

            # This node has sub-nodes and maybe an end-node.
            # eg. us -> (us, gov.us)
            if '_END' in node:
                if index < len(labels):
                    # check if there is a sub node
                    # eg. gov.us
                    if label in node:
                        suffix.append(label)
                        node = node[label]
                        continue
                if node['_END'] is True and label in node:
                    # check if it is an end-node
                    # eg. us
                    suffix.append(label)
                    break

            if '*' in node:
                if index < len(labels):
                    # check if there is a sub node
                    # eg. www.ck
                    if '!'+label in node:
                        ret_domain = label
                    else:
                        suffix.append(label)
                    break

            # check a TLD in PSL
            if label in node:
                suffix.append(label)
                node = node[label]
            else:
                break

        suffix.reverse()
        len_suffix = len(suffix)
        len_labels = len(labels)
        ret_suffix = ".".join(suffix)

        if len_suffix < len_labels and len_suffix != 0:
            ret_domain = labels[len_suffix]
            if subdomain:
                if len_suffix + 1 < len_labels:
                    ret_subdomain = input[:-(len(ret_domain + ret_suffix) + 2)]
        if ret_domain and ret_suffix:
            ret_domain_name = "%s.%s" % (ret_domain, ret_suffix)

        return (ret_subdomain,
                ret_domain,
                ret_suffix,
                ret_domain_name
                )

    def format(self, input):
        """
        Now we provide simple rules to format strings.
        eg. lower case, punycode transform
        Todo: 
        1.URL Parser to extract domain.
        2.idna domain parser
        :param input: 
        :return: input
        """
        input = input.strip().lower()
        input = idna.encode(input)
        # input = urlparse.urlparse(input).netloc
        # if '//' in input:
        #     _, _, input = input.rpartition('//')
        # if '/' in input:
        #     input, _, _ = input.lpartition('//')
        # Punycode costs too much time! Make sure you really need it.

        return input
