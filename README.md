# fasttld

[![PyPI version](https://badge.fury.io/py/fasttld.svg)](https://badge.fury.io/py/fasttld)
[![Build Status](https://api.travis-ci.org/jophy/fasttld.svg?branch=master)](https://travis-ci.org/jophy/fasttld)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

**fasttld** is a high performance [top level domains (TLD)](https://en.wikipedia.org/wiki/Top-level_domain) extraction module based on the compressed [trie](https://en.wikipedia.org/wiki/Trie) data structure
implemented with the builtin python `dict()`.

![Trie](https://upload.wikimedia.org/wikipedia/commons/b/be/Trie_example.svg)

## Background

The goal of **fasttld** is to extract [top level domains (TLDs)](https://en.wikipedia.org/wiki/Top-level_domain) from [URLs](https://en.wikipedia.org/wiki/URL) efficiently. In the other words, we extract `com` from URLs like `www.google.com` or `https://maps.google.com:8080/a/long/path/?query=42`.

Running something like **".".join(domain.split('.')[1::])** is not a viable solution, for example, `maps.baidu.com.cn`
would give us the wrong result `baidu.com.cn` instead of `com.cn`.

The **fasttld** module solves this problem by using the regularly-updated [Mozilla Public Suffix List](http://www.publicsuffix.org) and the [trie](https://en.wikipedia.org/wiki/Trie) data structure to efficiently extract subdomains, hostnames, and TLDs from URLs.

**fasttld** also supports extraction of private domains listed in the [Mozilla Public Suffix List](http://www.publicsuffix.org) like 'blogspot.co.uk' and 'sinaapp.com'.

## Installation

You can install fasttld from PyPI.

```python
pip install fasttld
```

or build from source

```python
git clone https://github.com/jophy/fasttld.git && cd fasttld
python setup.py install
```

## Usage

```python
>>> from fasttld import FastTLDExtract
>>> t = FastTLDExtract()
>>> res = t.extract("www.google.com")
>>> res
('www', 'google', 'com', 'google.com')
>>> subdomain, domain, suffix, domain_name = res
>>> subdomain
'www'
>>> domain
'google'
>>> suffix
'com'
>>> domain_name
'google.com'
```

extract() returns a tuple `(subdomain, domain, suffix, domain_name)` .

## Update the Mozilla Public Suffix List local copy

Whenever **fasttld** is called, it will automatically update the local copy of the Mozilla Public Suffix List if it is more than 3 days old.
You can also run the update process manually via the following commands.

```python
>>> import fasttld
>>> fasttld.update()
```

or

```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract().update()
```

## Specify Mozilla Public Suffix List file

You can also specify your own public suffix list file.

```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract(file_path='/path/to/psl/file').extract('domain', subdomain=False)
```

## Disable subdomain output

If you do not need to extract subdomains, you can disable subdomain output with `subdomain=False`.

```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract().extract('domain', subdomain=False) # set subdomain=False
```

## Optional: Exclude private domains

According to the [Mozilla.org wiki](https://wiki.mozilla.org/Public_Suffix_List/Uses), the Mozilla Public Suffix List contains private domains like `blogspot.co.uk` and `sinaapp.com` because some registered domain owners wish to delegate subdomains to mutually-untrusting parties, and find that being added to the PSL gives their solution more favourable security properties.

By default, **fasttld** treats private domains as TLDs (i.e. `exclude_private_suffix=False`)

```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract(exclude_private_suffix=False).extract('news.blogspot.co.uk')
>>> ('', 'news', 'blogspot.co.uk', 'news.blogspot.co.uk') # blogspot.co.uk is treated as a TLD
>>> FastTLDExtract().extract('news.blogspot.co.uk')  # this is the default behaviour
>>> ('', 'news', 'blogspot.co.uk', 'news.blogspot.co.uk') # same output as above
```

You can instruct **fasttld** to exclude private domains by setting `exclude_private_suffix=True`

```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract(exclude_private_suffix=True).extract('news.blogspot.co.uk') # set exclude_private_suffix=True
>>> ('news', 'blogspot', 'co.uk', 'blogspot.co.uk') # notice that co.uk is now recognised as the TLD instead of blogspot.co.uk
```

## Speed Comparison

Similar modules include [tldextract](https://github.com/john-kurkowski/tldextract) and [tld](https://github.com/barseghyanartur/tld).

### Test conditions

Initialize the module class once, then call its extract function ten million times. Measure the time taken.

### Test environment

Python 3.9.12, AMD Ryzen 7 5800X 3.8 GHz 8 cores 16 threads, 48GB RAM

### Test results

| **module\case** | `jophy.com` | `www.baidu.com.cn` | `jo.noexist` | `https://maps.google.com.ua/a/long/path?query=42` | `1.1.1.1` | `https://192.168.55.1` |
|-----------------|---------------|----------------------|----------------|-----------------------------------------------------|-------------|--------------------------|
| fasttld         | 7.60s         | 9.90s                | 5.28s          | 5.67s                                               | 5.06s       | 5.30s                    |
| tldextract      | 22.96s        | 29.32s               | 25.06s         | 31.69s                                              | 33.89s      | 35.15s                   |
| tld             | 26.75s        | 29.00s               | 23.01s         | 27.55s                                              | 22.79s      | 22.55s                   |

---

Excluding subdomains (i.e. `subdomain=False`)

| **module\case** | `jophy.com` | `www.baidu.com.cn` | `jo.noexist` | `https://maps.google.com.ua/a/long/path?query=42` | `1.1.1.1` | `https://192.168.55.1`
|-----------------|---------------|----------------------|----------------|-----------------------------------------------------|-------------|--------------------------|
| fasttld         | 7.55s         | 8.98s                | 5.20s          | 5.52s                                               | 5.13s       | 5.25s                    |

On average, **fasttld** is **4 to 5** times faster than the other modules. It retains its performance advantage even when parsing long URLs like `https://maps.google.com.ua/a/long/path?query=42`

## Acknowledgements

- Some code borrowed from the [tldextract](https://github.com/john-kurkowski/tldextract) module
