# fasttld
`Fasttld` is a high performance TLD extract module based on a compressed [trie](https://en.wikipedia.org/wiki/Trie) 
with builtin python dict().

![Trie](https://upload.wikimedia.org/wikipedia/commons/b/be/Trie_example.svg)

# Background
The plan of fasttld module is to extract top level domains from millions lines of domains (from DNS data) in one time. 
In the other words, we extract "www.google.com" into "google.com". 
 
Most programmers think it is easy, just run `".".join(domain.split('.')[1::])`. But it is wrong ! Think about how to 
process "www.baidu.com.cn". So we must know what suffixes are.

Thanks to [Mozilla Public Suffix List](http://www.publicsuffix.org), it provides us with all suffixes list, including 
some private domains such like 'blogspot.co.uk', 'sinaapp.com'.

# Install
You can install fasttld through PyPI.
```python
pip install fasttld
```
or
```python
git clone https://github.com/jophy/fasttld.git && cd fasttld
python setup.py
```

# Basic Usage
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
extract() returns a tupple (subdomain, domain, suffix, domain_name) .

# Update Public Suffix List
`fasttld` will update Public Suffix List every 3 days automatically when it is called.
You can also do update manually. Try the following commands.
```python
>>> import fasttld
>>> fasttld.update()
```
or
```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract().update()
```

# Specify Public Suffix List file
You can specify your own public suffix list file. Samples see bellow.
```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract(file_path='/path/to/psl/file').extract('domain', subdomain=False)
```

# Disable subdomain output
You can disable subdomain output, this action can accelerate 0.3s per million times extracting.Samples see bellow.
```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract().extract('domain', subdomain=False)
```
# Exclude private domain
Due to security issues, public suffix list contains some private domains. Eg, blogspot.co.uk, sinaapp.com.

`fasttld` can exclude private domain at the beginning of constructing the suffix trie. Samples see bellow.

```python
>>> from fasttld import FastTLDExtract
>>> FastTLDExtract(exclude_private_suffix=True).extract('news.blogspot.co.uk')
>>> ('news', 'blogspot', 'co.uk', 'blogspot.co.uk')
>>> FastTLDExtract(exclude_private_suffix=False).extract('news.blogspot.co.uk')
>>> ('', 'news', 'blogspot.co.uk', 'news.blogspot.co.uk')
>>> FastTLDExtract().extract('news.blogspot.co.uk')  # default
>>> ('', 'news', 'blogspot.co.uk', 'news.blogspot.co.uk')
```

# Comparison
Comparing with the similar modules, eg, [tldextract](https://github.com/john-kurkowski/tldextract) , 
[tld](https://github.com/barseghyanartur/tld). 

Initialize the class just one time, calling extract function one million times. Results see below.

Test environment: Macbook Pro 13', Intel Core i5 2.7 GHz, 8GB RAM.


 module\case | jophy.com | www.baidu.com.cn|jo.noexist
-------------|-----------|-----------------|----------
fasttld      |    2.93   |       3.37      |  1.86
tldextract   |    8.68   |      11.69      |  9.22
tld          |   11.50   |      11.15      |  12.06

Disable subdomain output:

 module\case | jophy.com | www.baidu.com.cn|jo.noexist
-------------|-----------|-----------------|----------
fasttld      |    2.73   |       3.08      |  1.90

`fasttld` is **five** times faster than the other modules.

# License
GPL 3.0