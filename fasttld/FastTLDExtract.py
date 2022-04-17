#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jophy and Wu Tingfeng
@file: psl.py

Copyright (c) 2022 Wu Tingfeng
Copyright (c) 2017-2018 Jophy
"""
import re
import socket

import idna

from fasttld.psl import getPublicSuffixList, update

IP_RE = re.compile(
    r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
    r"([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
)

# Characters valid in scheme names
SCHEME_RE = re.compile(r"^[A-Za-z0-9+-.]+://")


def looks_like_ip(maybe_ip):
    """Does the given str look like an IP address?"""
    try:
        socket.inet_aton(maybe_ip)
        return True
    except socket.error:  # for Python 2 compatibility
        pass
    except (AttributeError, UnicodeError):
        if IP_RE.match(maybe_ip):
            return True

    return False


class FastTLDExtract(object):
    def __init__(self, exclude_private_suffix=False, file_path=""):
        self.trie = self._trie_construct(exclude_private_suffix, file_path)

    def update(self, *args, **kwargs):
        update(*args, **kwargs)

    def nested_dict(self, dic, keys):
        """
        The idea of this function is based on https://stackoverflow.com/questions/13687924
        :param dic:
        :param keys:
        :return:
        """
        end = False
        for key in keys[:-1]:
            dic_bk = dic
            if key not in dic:
                dic[key] = {}
            dic = dic[key]
            if isinstance(dic, bool):
                end = True
                dic = dic_bk
                dic[keys[-2]] = {"_END": True, keys[-1]: True}
        if not end:
            dic[keys[-1]] = True

    def _trie_construct(self, exclude_private_suffix, file_path=""):
        """
        This function for building a trie structure based on Mozilla Public Suffix List.
        In order to construct this, all suffixes sorted in a reverse order.
        For example, www.google.com -> com.google.www
        :return: a trie dict
        """
        tld_trie = {}
        PublicSuffixList, PrivateSuffixList, AllSuffixList = getPublicSuffixList(file_path)
        SuffixList = PublicSuffixList if exclude_private_suffix else AllSuffixList
        for suffix in SuffixList:
            if "." in suffix:
                sp = suffix.split(".")
                sp.reverse()
                self.nested_dict(tld_trie, sp)
            else:
                tld_trie[suffix] = {"_END": True}
        for key, val in tld_trie.items():
            if len(val) == 1 and "_END" in val:
                tld_trie[key] = True
        return tld_trie

    def __call__(self, *args, **kwargs):
        return self.extract(*args, **kwargs)

    def extract(self, raw_url, subdomain=True, format=False):
        """
        Extract suffix and subdomain from a Domain.
        :param raw_url:
        :param subdomain: Output options. This option will reduce efficiency. Maybe 10%
        :param format: To format raw_url string.
        :return: Tuple(subdomain, domain, suffix, domain_name)
        >>> FastTLDExtract.extract('www.google.com.hk', subdomain=True)
        >>> ('www', 'google', 'com.hk', 'google.com.hk')

        >>> FastTLDExtract.extract('127.0.0.1', subdomain=True)
        >>> ('', '127.0.0.1', '', '127.0.0.1')
        """
        ret_subdomain = ret_domain = ret_suffix = ret_domain_name = ""
        if format:
            raw_url = self.format(raw_url)

        # Borrowed from tldextract library (https://github.com/john-kurkowski/tldextract)
        # Use regex to strip raw_url of scheme subcomponent and anything after host subcomponent
        # Reference: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Syntax
        netloc = (
            SCHEME_RE.sub("", raw_url)
            .partition("/")[0]
            .partition("?")[0]
            .partition("#")[0]
            .split("@")[-1]
            .partition(":")[0]
            .strip()
            .rstrip(".")
        )
        # Determine if raw_url is an IP address
        if len(netloc) != 0 and looks_like_ip(netloc):
            return ("", netloc, "", netloc)
        labels = netloc.split(".")
        labels.reverse()
        node = self.trie  # define the root node
        suffix = []
        for label in labels:
            if node is True:  # or alternatively if type(node) is not dict:
                # This node is an end node.
                ret_domain = label
                break

            # This node has sub-nodes and maybe an end-node.
            # eg. cn -> (cn, gov.cn)
            if "_END" in node:
                # check if there is a sub node
                # eg. gov.cn
                if label in node:
                    suffix.append(label)
                    node = node[label]
                    continue

            if "*" in node:
                # check if there is a sub node
                # eg. www.ck
                if ("!%s" % label) in node:
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

        if 0 < len_suffix < len_labels:
            ret_domain = labels[len_suffix]
            if subdomain:
                if len_suffix + 1 < len_labels:
                    ret_subdomain = netloc[: -(len(ret_domain) + len(ret_suffix) + 2)]
        if ret_domain and ret_suffix:
            ret_domain_name = "%s.%s" % (ret_domain, ret_suffix)

        return (ret_subdomain, ret_domain, ret_suffix, ret_domain_name)

    def format(self, raw_url):
        """
        Now we provide simple rules to format strings.
        eg. lower case, punycode transform
        Todo:
        1.URL Parser to extract domain.
        2.idna domain parser
        :param raw_url:
        :return: input
        """
        # idna_url = idna.encode(raw_url.strip().lower()).decode()
        # input_ = urlparse.urlparse(idna_url).netloc
        # if '//' in input_:
        #     _, _, input_ = input_.rpartition('//')
        # if '/' in input_:
        #     input_, _, _ = input_.lpartition('//')
        # return input_
        # Punycode costs too much time! Make sure you really need it.

        return idna.encode(raw_url.strip().lower()).decode()
